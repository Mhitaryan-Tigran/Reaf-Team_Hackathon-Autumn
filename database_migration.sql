-- Database Migration for Host Checker
-- Production-ready schema for Railway PostgreSQL

-- =============================================
-- TABLES
-- =============================================

-- Agents table
CREATE TABLE IF NOT EXISTS agents (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    api_token VARCHAR(64) NOT NULL UNIQUE,
    ip_address VARCHAR(45),
    status VARCHAR(20) DEFAULT 'offline',
    last_heartbeat TIMESTAMP,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    
    CONSTRAINT agents_status_check CHECK (status IN ('online', 'offline'))
);

-- Checks table
CREATE TABLE IF NOT EXISTS checks (
    id VARCHAR(36) PRIMARY KEY,
    target VARCHAR(500) NOT NULL,
    check_types JSONB NOT NULL,
    agent_ids JSONB DEFAULT '[]'::jsonb,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    CONSTRAINT checks_status_check CHECK (status IN ('pending', 'in_progress', 'completed', 'failed'))
);

-- Check results table
CREATE TABLE IF NOT EXISTS check_results (
    id VARCHAR(36) PRIMARY KEY,
    check_id VARCHAR(36) NOT NULL,
    agent_id VARCHAR(36) NOT NULL,
    check_type VARCHAR(50) NOT NULL,
    success BOOLEAN NOT NULL,
    data JSONB DEFAULT '{}'::jsonb,
    error TEXT,
    duration_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_check FOREIGN KEY (check_id) REFERENCES checks(id) ON DELETE CASCADE,
    CONSTRAINT fk_agent FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE
);

-- =============================================
-- INDEXES for performance
-- =============================================

-- Agents indexes
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_agents_last_heartbeat ON agents(last_heartbeat);
CREATE INDEX IF NOT EXISTS idx_agents_location ON agents(location);

-- Checks indexes
CREATE INDEX IF NOT EXISTS idx_checks_status ON checks(status);
CREATE INDEX IF NOT EXISTS idx_checks_created_at ON checks(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_checks_target ON checks(target);

-- Check results indexes
CREATE INDEX IF NOT EXISTS idx_check_results_check_id ON check_results(check_id);
CREATE INDEX IF NOT EXISTS idx_check_results_agent_id ON check_results(agent_id);
CREATE INDEX IF NOT EXISTS idx_check_results_created_at ON check_results(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_check_results_success ON check_results(success);

-- JSONB indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_checks_check_types_gin ON checks USING GIN (check_types);
CREATE INDEX IF NOT EXISTS idx_check_results_data_gin ON check_results USING GIN (data);
CREATE INDEX IF NOT EXISTS idx_agents_metadata_gin ON agents USING GIN (metadata);

-- =============================================
-- FUNCTIONS & TRIGGERS
-- =============================================

-- Function to automatically update check status
CREATE OR REPLACE FUNCTION update_check_status() RETURNS TRIGGER AS $$
BEGIN
    -- If all expected results are in, mark check as completed
    DECLARE
        expected_count INTEGER;
        actual_count INTEGER;
    BEGIN
        SELECT 
            (SELECT COUNT(*) FROM jsonb_array_elements_text(c.check_types)) *
            (SELECT COUNT(*) FROM jsonb_array_elements_text(c.agent_ids))
        INTO expected_count
        FROM checks c
        WHERE c.id = NEW.check_id;
        
        SELECT COUNT(*) INTO actual_count
        FROM check_results
        WHERE check_id = NEW.check_id;
        
        IF actual_count >= expected_count THEN
            UPDATE checks
            SET status = 'completed', completed_at = NOW()
            WHERE id = NEW.check_id AND status = 'in_progress';
        END IF;
    END;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger on check_results insert
DROP TRIGGER IF EXISTS trigger_update_check_status ON check_results;
CREATE TRIGGER trigger_update_check_status
    AFTER INSERT ON check_results
    FOR EACH ROW
    EXECUTE FUNCTION update_check_status();

-- =============================================
-- VIEWS for analytics
-- =============================================

-- View: Agent statistics
CREATE OR REPLACE VIEW agent_stats AS
SELECT 
    a.id,
    a.name,
    a.location,
    a.status,
    a.last_heartbeat,
    COUNT(DISTINCT cr.check_id) as total_checks_performed,
    COUNT(cr.id) as total_tasks_performed,
    AVG(cr.duration_ms) as avg_response_time_ms,
    SUM(CASE WHEN cr.success THEN 1 ELSE 0 END)::FLOAT / NULLIF(COUNT(cr.id), 0) * 100 as success_rate
FROM agents a
LEFT JOIN check_results cr ON a.id = cr.agent_id
GROUP BY a.id, a.name, a.location, a.status, a.last_heartbeat;

-- View: Recent check summary
CREATE OR REPLACE VIEW recent_checks_summary AS
SELECT 
    c.id,
    c.target,
    c.status,
    c.created_at,
    c.completed_at,
    c.check_types,
    COUNT(cr.id) as results_count,
    SUM(CASE WHEN cr.success THEN 1 ELSE 0 END) as success_count,
    AVG(cr.duration_ms) as avg_duration_ms
FROM checks c
LEFT JOIN check_results cr ON c.id = cr.check_id
GROUP BY c.id, c.target, c.status, c.created_at, c.completed_at, c.check_types
ORDER BY c.created_at DESC
LIMIT 100;

-- =============================================
-- CLEANUP FUNCTIONS
-- =============================================

-- Function to clean up old checks (older than 30 days)
CREATE OR REPLACE FUNCTION cleanup_old_checks(days_to_keep INTEGER DEFAULT 30) RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM checks
    WHERE created_at < NOW() - (days_to_keep || ' days')::INTERVAL
    AND status = 'completed';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Function to mark offline agents
CREATE OR REPLACE FUNCTION mark_offline_agents(timeout_seconds INTEGER DEFAULT 60) RETURNS INTEGER AS $$
DECLARE
    updated_count INTEGER;
BEGIN
    UPDATE agents
    SET status = 'offline'
    WHERE last_heartbeat < NOW() - (timeout_seconds || ' seconds')::INTERVAL
    AND status = 'online';
    
    GET DIAGNOSTICS updated_count = ROW_COUNT;
    RETURN updated_count;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- SAMPLE DATA (for testing, remove in production)
-- =============================================

-- Insert sample agent (uncomment for testing)
-- INSERT INTO agents (id, name, location, api_token, status)
-- VALUES (
--     'sample-agent-moscow-001',
--     'Test Agent Moscow',
--     'Russia, Moscow',
--     'test-token-' || md5(random()::text),
--     'offline'
-- ) ON CONFLICT (id) DO NOTHING;

-- =============================================
-- GRANTS (adjust based on your user setup)
-- =============================================

-- Grant permissions to application user
-- GRANT SELECT, INSERT, UPDATE, DELETE ON agents, checks, check_results TO hostchecker_app;
-- GRANT SELECT ON agent_stats, recent_checks_summary TO hostchecker_app;
-- GRANT EXECUTE ON FUNCTION cleanup_old_checks, mark_offline_agents TO hostchecker_app;

-- =============================================
-- MAINTENANCE QUERIES
-- =============================================

-- Get database statistics
-- SELECT 
--     table_name,
--     pg_size_pretty(pg_total_relation_size(quote_ident(table_name))) AS size
-- FROM information_schema.tables
-- WHERE table_schema = 'public'
-- ORDER BY pg_total_relation_size(quote_ident(table_name)) DESC;

-- Check index usage
-- SELECT 
--     schemaname,
--     tablename,
--     indexname,
--     idx_scan as index_scans,
--     idx_tup_read as tuples_read,
--     idx_tup_fetch as tuples_fetched
-- FROM pg_stat_user_indexes
-- ORDER BY idx_scan DESC;

-- Clean up old checks (example: keep last 30 days)
-- SELECT cleanup_old_checks(30);

-- Mark offline agents
-- SELECT mark_offline_agents(60);

