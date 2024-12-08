"""Test cases for model validation"""

TEST_CASES = [
    # Development (10 cases)
    ("Add login feature", "Implement user authentication"),
    ("Create REST API", "Build backend endpoints"),
    ("Implement websockets", "Add real-time communication"),
    ("Build payment gateway", "Implement stripe integration"),
    ("Create GraphQL API", "Implement GraphQL resolvers"),
    ("Add social login", "Implement OAuth authentication"),
    ("Create microservice", "Build new service architecture"),
    ("Implement caching", "Add Redis caching layer"),
    ("Build search service", "Implement Elasticsearch integration"),
    ("Create webhook system", "Implement webhook handlers"),
    
    # Bug Fix (10 cases)
    ("Fix login crash", "Debug authentication failure"),
    ("Fix memory leak", "Resolve memory consumption issue"),
    ("Fix data corruption", "Resolve data integrity issues"),
    ("Fix infinite loop", "Debug endless processing issue"),
    ("Fix race condition", "Resolve concurrent access bug"),
    ("Fix API timeout", "Debug slow endpoint response"),
    ("Fix database deadlock", "Resolve transaction blocking"),
    ("Fix cache invalidation", "Debug stale cache issues"),
    ("Fix session handling", "Resolve session expiry problems"),
    ("Fix connection pool", "Debug connection leaks"),
    
    # Feature (10 cases)
    ("Add dark mode", "Implement theme switching"),
    ("Add notifications", "Implement push notifications"),
    ("Add export feature", "Enable data exporting"),
    ("Add chat system", "Implement real-time messaging"),
    ("Add analytics", "Implement usage tracking"),
    ("Add file upload", "Enable document uploading"),
    ("Add search filters", "Implement advanced search"),
    ("Add bulk actions", "Enable batch operations"),
    ("Add commenting", "Implement discussion system"),
    ("Add favorites", "Enable content bookmarking"),
    
    # Documentation (10 cases)
    ("Update API docs", "Document new endpoints"),
    ("Write setup guide", "Create installation documentation"),
    ("Document workflows", "Explain development processes"),
    ("API reference", "Create comprehensive API documentation"),
    ("Update changelog", "Document version changes"),
    ("Create user guide", "Write end-user documentation"),
    ("Document architecture", "Create system architecture docs"),
    ("Write contribution guide", "Document contribution process"),
    ("Create style guide", "Document coding standards"),
    ("API examples", "Add example API usage"),
    
    # Enhancement (10 cases)
    ("Improve error handling", "Better error messages"),
    ("Optimize queries", "Improve database performance"),
    ("Refactor components", "Clean up component logic"),
    ("Enhance validation", "Improve input validation"),
    ("Improve logging", "Enhanced error tracking"),
    ("Optimize images", "Better image processing"),
    ("Enhance search", "Improve search results"),
    ("Refactor API", "Clean up API structure"),
    ("Improve caching", "Better cache management"),
    ("Enhance monitoring", "Better system monitoring"),
    
    # Security (10 cases)
    ("Add rate limiting", "Prevent brute force attacks"),
    ("Implement 2FA", "Add two-factor authentication"),
    ("Security audit", "Review security vulnerabilities"),
    ("Update dependencies", "Fix security vulnerabilities"),
    ("Add encryption", "Implement data encryption"),
    ("Security headers", "Add security headers"),
    ("Access control", "Implement role permissions"),
    ("Audit logging", "Track security events"),
    ("Vulnerability scan", "Check for vulnerabilities"),
    ("Password policy", "Enforce strong passwords"),
    
    # Performance (10 cases)
    ("Optimize loading", "Improve page load time"),
    ("Cache responses", "Implement API caching"),
    ("Database tuning", "Optimize database settings"),
    ("Reduce bundle size", "Optimize JavaScript bundle"),
    ("Memory optimization", "Reduce memory usage"),
    ("Query optimization", "Improve database queries"),
    ("Asset compression", "Optimize static assets"),
    ("Load balancing", "Distribute server load"),
    ("CDN integration", "Implement content delivery"),
    ("Response time", "Improve API latency"),
    
    # Testing (10 cases)
    ("Add unit tests", "Write component tests"),
    ("E2E testing", "Implement end-to-end tests"),
    ("Integration tests", "Add service integration tests"),
    ("Performance testing", "Implement load tests"),
    ("Security testing", "Add penetration tests"),
    ("API testing", "Test endpoint functionality"),
    ("Regression tests", "Add regression test suite"),
    ("Browser testing", "Test cross-browser compatibility"),
    ("Mobile testing", "Test mobile compatibility"),
    ("Stress testing", "Test system under load"),
    
    # UI/UX (10 cases)
    ("Improve mobile UI", "Better mobile experience"),
    ("Update color scheme", "Implement new brand colors"),
    ("Form redesign", "Improve form layout"),
    ("Enhance accessibility", "Add ARIA labels"),
    ("Responsive design", "Improve mobile layout"),
    ("Navigation update", "Improve menu structure"),
    ("Dashboard layout", "Improve dashboard UI"),
    ("Error messages", "Improve error displays"),
    ("Loading states", "Add loading indicators"),
    ("Input feedback", "Improve user feedback"),
    
    # DevOps (10 cases)
    ("Setup CI/CD", "Configure GitHub Actions"),
    ("Docker setup", "Create container configuration"),
    ("AWS setup", "Configure cloud infrastructure"),
    ("Kubernetes deploy", "Setup K8s cluster"),
    ("Monitoring setup", "Configure system monitoring"),
    ("Backup system", "Setup automated backups"),
    ("Log aggregation", "Setup centralized logging"),
    ("Auto scaling", "Configure auto scaling"),
    ("Deploy scripts", "Create deployment automation"),
    ("Environment setup", "Configure development environment"),
    
    # Design (10 cases)
    ("Design system", "Create component library"),
    ("Mobile mockups", "Create app interface designs"),
    ("Typography system", "Design font hierarchy"),
    ("Dashboard design", "Create analytics dashboard"),
    ("Icon system", "Design custom icon set"),
    ("Color palette", "Define brand colors"),
    ("Component design", "Create UI components"),
    ("Layout system", "Design grid system"),
    ("Animation design", "Create motion system"),
    ("Error states", "Design error displays"),
    
    # Research (10 cases)
    ("Evaluate frameworks", "Research frontend frameworks"),
    ("Database options", "Research database solutions"),
    ("Security tools", "Research security options"),
    ("Cloud providers", "Compare cloud services"),
    ("AI solutions", "Research machine learning options"),
    ("Analytics tools", "Research analytics platforms"),
    ("Testing frameworks", "Evaluate testing tools"),
    ("Monitoring solutions", "Research monitoring tools"),
    ("Payment providers", "Compare payment services"),
    ("Search engines", "Evaluate search solutions"),
    
    # Meeting (10 cases)
    ("Weekly standup", "Team sync meeting"),
    ("Sprint planning", "Plan next sprint"),
    ("Design review", "Review design changes"),
    ("Client meeting", "Product demo with stakeholders"),
    ("Tech talk", "Internal knowledge sharing"),
    ("Team retro", "Sprint retrospective"),
    ("Architecture review", "Review system design"),
    ("Status update", "Project status meeting"),
    ("Code review", "Review code changes"),
    ("Product demo", "Demonstrate features"),
    
    # Planning (10 cases)
    ("Q2 roadmap", "Plan next quarter"),
    ("Resource planning", "Allocate team resources"),
    ("Sprint schedule", "Plan sprint activities"),
    ("Release planning", "Plan version deployment"),
    ("Project timeline", "Create project schedule"),
    ("Feature planning", "Plan feature development"),
    ("Team planning", "Plan team assignments"),
    ("Budget planning", "Plan project budget"),
    ("Risk planning", "Identify project risks"),
    ("Capacity planning", "Plan team capacity"),
    
    # Other (10 cases)
    ("Team training", "Knowledge sharing session"),
    ("Process improvement", "Improve workflows"),
    ("Asset management", "Manage project assets"),
    ("Vendor review", "Evaluate third-party services"),
    ("License audit", "Review software licenses"),
    ("Team building", "Organize team activity"),
    ("Office setup", "Configure work environment"),
    ("Resource tracking", "Track resource usage"),
    ("Compliance check", "Review compliance requirements"),
    ("Knowledge transfer", "Share project knowledge")
]

# Comprehensive edge cases for testing
EDGE_CASES = [
    # Mixed categories (multiple strong signals)
    ("Design and implement API", "Create and develop REST endpoints"),
    ("Security testing implementation", "Develop and test security measures"),
    ("Document new feature", "Write documentation for new functionality"),
    ("Performance testing framework", "Develop and test performance metrics"),
    ("DevOps security setup", "Implement secure deployment pipeline"),
    ("UI/UX development", "Implement new user interface design"),
    ("Research and implement", "Investigate and build new solution"),
    ("Plan and document", "Create project plan and documentation"),
    
    # Ambiguous cases (weak signals)
    ("System update", "Update project components"),
    ("General improvements", "Various system enhancements"),
    ("Project maintenance", "Regular system upkeep"),
    ("Review changes", "Check recent updates"),
    ("Update system", "Make necessary changes"),
    
    # Short inputs
    ("Fix bug", "Debug issue"),
    ("Meeting", "Team sync"),
    ("Update", "Changes"),
    ("Check", "Verify"),
    ("Review", "Assess"),
    
    # Long inputs
    ("Comprehensive system architecture redesign and implementation", 
     "Complete overhaul of existing system architecture including database, API, and frontend components"),
    ("Full-scale security audit and implementation of recommended security measures",
     "Conduct thorough security review and implement all necessary security improvements across the platform"),
    ("Enterprise-wide performance optimization and monitoring solution implementation",
     "Design and implement comprehensive performance monitoring and optimization across all system components"),
    
    # Special characters
    ("Fix login/auth bug", "Debug authentication/authorization issue"),
    ("Update API (v2)", "Implement new API version"),
    ("CI/CD & Testing", "Setup pipeline and tests"),
    ("Research & Development", "Investigate new technologies"),
    ("UI/UX Enhancement", "Improve user interface/experience"),
    
    # Multiple categories with equal weight
    ("Security and Performance", "Optimize and secure system"),
    ("Design and Development", "Create and build feature"),
    ("Testing and Documentation", "Test and document system"),
    ("Research and Planning", "Investigate and plan implementation"),
    
    # Time-based tasks
    ("Q4 2024 Planning", "Plan next year activities"),
    ("Weekly Maintenance", "Regular system updates"),
    ("Daily Checks", "Routine system verification"),
    
    # Priority indicators
    ("URGENT: Fix crash", "Critical system failure"),
    ("HIGH: Security patch", "Important security update"),
    ("LOW: Update docs", "Minor documentation changes")
] 