import pytest
from smartsynch.models.predictor import MLPredictor
import joblib

@pytest.fixture
def predictor():
    from smartsynch.train import get_training_data
    pred = MLPredictor()
    
    # Get training data and labels
    training_data, _ = get_training_data()  # We don't need the labels since train() determines them internally
    
    # Train the model
    pred.train(training_data)  # train() expects List[Tuple[str, str]]
    return pred

def test_development_prediction(predictor):
    """Test development task predictions"""
    result = predictor.predict(
        "Add login feature",
        "Implement user authentication"
    )
    assert result["category"] == "Development"
    assert 80.0 <= result["confidence"] <= 100.0

def test_meeting_prediction(predictor):
    """Test meeting task predictions"""
    result = predictor.predict(
        "Weekly standup",
        "Team sync meeting"
    )
    assert result["category"] == "Meeting"
    assert 80.0 <= result["confidence"] <= 100.0

def test_research_prediction(predictor):
    """Test research task predictions"""
    result = predictor.predict(
        "Investigate performance",
        "Research system bottlenecks"
    )
    assert result["category"] == "Research"
    assert 80.0 <= result["confidence"] <= 100.0

def test_design_prediction(predictor):
    """Test design task predictions"""
    result = predictor.predict(
        "UI/UX improvements",
        "Design user interface"
    )
    assert result["category"] == "Design"
    assert 80.0 <= result["confidence"] <= 100.0

def test_planning_prediction(predictor):
    """Test planning task predictions"""
    result = predictor.predict(
        "Sprint planning",
        "Plan next sprint"
    )
    assert result["category"] == "Planning"
    assert 80.0 <= result["confidence"] <= 100.0

def test_edge_cases(predictor):
    """Test edge cases"""
    # Empty input
    result = predictor.predict("", "")
    assert isinstance(result["category"], str)
    assert isinstance(result["confidence"], float)

    # Very short input
    result = predictor.predict("test", "quick")
    assert isinstance(result["category"], str)
    assert isinstance(result["confidence"], float)

    # Very long input
    long_text = "very " * 100
    result = predictor.predict(long_text, long_text)
    assert isinstance(result["category"], str)
    assert isinstance(result["confidence"], float)

def test_batch_predictions(predictor):
    """Test batch prediction functionality"""
    tasks = [
        ("Add feature", "Implement new functionality"),
        ("Team meeting", "Weekly sync"),
        ("Research API", "Investigate new technology")
    ]
    results = predictor.batch_predict(tasks)
    assert len(results) == len(tasks)
    for result in results:
        assert "category" in result
        assert "confidence" in result
        assert isinstance(result["confidence"], float)
        assert 0.0 <= result["confidence"] <= 100.0

def test_mixed_category_detection(predictor):
    """Test detection of tasks that might belong to multiple categories"""
    result = predictor.predict(
        "Design and implement API",
        "Create and develop REST endpoints"
    )
    # Should detect either Design or Development with lower confidence
    assert result["category"] in ["Design", "Development"]
    assert result["confidence"] <= 95.0  # Lower confidence due to mixed signals
    assert result["confidence"] >= 70.0  # But still reasonably confident

def test_keyword_scoring(predictor):
    """Test the keyword scoring mechanism"""
    # Test with strong keywords
    result = predictor.predict(
        "Implement new feature",
        "Develop and code functionality"
    )
    assert result["category"] == "Development"
    assert result["confidence"] > 90.0  # High confidence due to strong keywords

    # Test with weak keywords
    result = predictor.predict(
        "Update something",
        "Create new thing"
    )
    assert isinstance(result["category"], str)
    assert result["confidence"] < 90.0  # Lower confidence due to weak keywords

def test_model_persistence(predictor, tmp_path):
    """Test model saving and loading"""
    # Save the model
    model_path = tmp_path / "test_model.joblib"
    joblib.dump(predictor.pipeline, model_path)
    
    # Create new predictor and load the model
    new_predictor = MLPredictor()
    new_predictor.pipeline = joblib.load(model_path)
    
    # Test prediction with loaded model
    result = new_predictor.predict(
        "Add feature",
        "Implement functionality"
    )
    assert isinstance(result["category"], str)
    assert isinstance(result["confidence"], float) 
def test_design_predictions(predictor):
    """Test various design-related tasks"""
    design_tests = [
        # Pure design tasks
        (
            "Design login wireframes",
            "Create mockups for authentication screens",
            "Design",
            90.0
        ),
        (
            "UI/UX for dashboard",
            "Design user interface for analytics",
            "Design",
            90.0
        ),
        (
            "Design system update",
            "Update component library and style guide",
            "Design",
            90.0
        )
    ]
    
    for title, desc, expected_category, min_confidence in design_tests:
        result = predictor.predict(title, desc)
        assert result["category"] == expected_category, \
            f"Failed on: {title} - Expected {expected_category}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}" 

def test_bug_fix_prediction(predictor):
    """Test bug fix predictions"""
    result = predictor.predict(
        "Fix login crash",
        "Debug authentication failure"
    )
    assert result["category"] == "Bug_Fix"
    assert 80.0 <= result["confidence"] <= 100.0

def test_feature_prediction(predictor):
    """Test feature request predictions"""
    result = predictor.predict(
        "Add dark mode",
        "Implement theme switching"
    )
    assert result["category"] == "Feature"
    assert 80.0 <= result["confidence"] <= 100.0

def test_documentation_prediction(predictor):
    """Test documentation predictions"""
    result = predictor.predict(
        "Update API docs",
        "Document new endpoints"
    )
    assert result["category"] == "Documentation"
    assert 80.0 <= result["confidence"] <= 100.0

def test_security_prediction(predictor):
    """Test security task predictions"""
    result = predictor.predict(
        "Add rate limiting",
        "Prevent brute force attacks"
    )
    assert result["category"] == "Security"
    assert 80.0 <= result["confidence"] <= 100.0

def test_performance_prediction(predictor):
    """Test performance task predictions"""
    result = predictor.predict(
        "Optimize loading",
        "Improve page load time"
    )
    assert result["category"] == "Performance"
    assert 80.0 <= result["confidence"] <= 100.0

def test_performance_predictions(predictor):
    """Test performance-related tasks"""
    performance_tests = [
        (
            "Optimize Database Queries",
            "Review and optimize slow-performing SQL queries in analytics module",
            "Performance",
            90.0
        ),
        (
            "Bundle Size Optimization",
            "Reduce main bundle size using code splitting and lazy loading",
            "Performance",
            90.0
        ),
        (
            "API Response Time",
            "Improve endpoint latency to achieve sub-200ms responses",
            "Performance",
            90.0
        )
    ]
    
    for title, desc, expected_category, min_confidence in performance_tests:
        result = predictor.predict(title, desc)
        assert result["category"] == expected_category, \
            f"Failed on: {title} - Expected {expected_category}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}"

def test_devops_predictions(predictor):
    """Test DevOps-related tasks"""
    devops_tests = [
        (
            "Configure CI Pipeline",
            "Set up GitHub Actions workflow for testing and deployment",
            "DevOps",
            90.0
        ),
        (
            "Optimize Docker Build",
            "Reduce container image size and improve build times",
            "DevOps",
            90.0
        ),
        (
            "Setup Kubernetes",
            "Configure container orchestration for production",
            "DevOps",
            90.0
        )
    ]
    
    for title, desc, expected_category, min_confidence in devops_tests:
        result = predictor.predict(title, desc)
        assert result["category"] == expected_category, \
            f"Failed on: {title} - Expected {expected_category}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}"

def test_security_predictions(predictor):
    """Test security-related tasks"""
    security_tests = [
        (
            "Security Audit",
            "Review npm dependencies for vulnerabilities",
            "Security",
            90.0
        ),
        (
            "Implement Rate Limiting",
            "Add API rate limiting for brute force prevention",
            "Security",
            90.0
        ),
        (
            "CSRF Protection",
            "Implement cross-site request forgery tokens",
            "Security",
            90.0
        )
    ]
    
    for title, desc, expected_category, min_confidence in security_tests:
        result = predictor.predict(title, desc)
        assert result["category"] == expected_category, \
            f"Failed on: {title} - Expected {expected_category}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}"

def test_research_predictions(predictor):
    """Test research-related tasks"""
    research_tests = [
        (
            "Evaluate State Management",
            "Compare Redux alternatives for frontend",
            "Research",
            90.0
        ),
        (
            "Investigate PWA",
            "Research progressive web app implementation",
            "Research",
            90.0
        ),
        (
            "Cloud Provider Comparison",
            "Compare AWS vs GCP for infrastructure",
            "Research",
            90.0
        )
    ]
    
    for title, desc, expected_category, min_confidence in research_tests:
        result = predictor.predict(title, desc)
        assert result["category"] == expected_category, \
            f"Failed on: {title} - Expected {expected_category}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}"

def test_mixed_category_predictions(predictor):
    """Test tasks that might fall into multiple categories"""
    mixed_tests = [
        (
            "Optimize API Performance",
            "Improve endpoint response times and add caching",
            ["Performance", "Development"],
            85.0
        ),
        (
            "Security Performance Audit",
            "Analyze and optimize security measures impact on performance",
            ["Security", "Performance"],
            85.0
        ),
        (
            "DevOps Security Implementation",
            "Set up security scanning in CI/CD pipeline",
            ["DevOps", "Security"],
            85.0
        )
    ]
    
    for title, desc, expected_categories, min_confidence in mixed_tests:
        result = predictor.predict(title, desc)
        assert result["category"] in expected_categories, \
            f"Failed on: {title} - Expected one of {expected_categories}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}" 

def test_performance_edge_cases(predictor):
    """Test edge cases for performance-related tasks"""
    edge_cases = [
        (
            "Slow Loading Time",
            "Pages take > 3s to load on mobile devices",
            "Performance",
            85.0
        ),
        (
            "Memory Usage Spike",
            "Dashboard memory consumption increases over time",
            ["Performance", "Bug_Fix"],
            85.0
        ),
        (
            "Database Connection Pool",
            "Optimize connection pooling settings for better throughput",
            ["Performance", "DevOps"],
            85.0
        ),
        (
            "CDN Setup for Assets",
            "Configure CloudFront for static asset delivery",
            ["Performance", "DevOps"],
            85.0
        )
    ]
    
    for title, desc, expected, min_confidence in edge_cases:
        result = predictor.predict(title, desc)
        if isinstance(expected, list):
            assert result["category"] in expected, \
                f"Failed on: {title} - Expected one of {expected}, got {result['category']}"
        else:
            assert result["category"] == expected, \
                f"Failed on: {title} - Expected {expected}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}"

def test_security_edge_cases(predictor):
    """Test edge cases for security-related tasks"""
    edge_cases = [
        (
            "Penetration Test Findings",
            "Address critical vulnerabilities from pentest report",
            "Security",
            90.0
        ),
        (
            "Auth Token Expiry",
            "Fix token refresh mechanism in auth flow",
            ["Security", "Bug_Fix"],
            85.0
        ),
        (
            "Security Performance Impact",
            "Optimize encryption overhead in API calls",
            ["Security", "Performance"],
            85.0
        ),
        (
            "DevSecOps Integration",
            "Add security scanning to build pipeline",
            ["Security", "DevOps"],
            85.0
        )
    ]
    
    for title, desc, expected, min_confidence in edge_cases:
        result = predictor.predict(title, desc)
        if isinstance(expected, list):
            assert result["category"] in expected, \
                f"Failed on: {title} - Expected one of {expected}, got {result['category']}"
        else:
            assert result["category"] == expected, \
                f"Failed on: {title} - Expected {expected}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}"

def test_devops_edge_cases(predictor):
    """Test edge cases for DevOps-related tasks"""
    edge_cases = [
        (
            "Pipeline Timeout",
            "Fix CI/CD pipeline hanging on large builds",
            ["DevOps", "Bug_Fix"],
            85.0
        ),
        (
            "Terraform State Lock",
            "Fix state file locking in concurrent deployments",
            ["DevOps", "Bug_Fix"],
            85.0
        ),
        (
            "Container Resource Limits",
            "Optimize k8s pod resource allocation",
            ["DevOps", "Performance"],
            85.0
        ),
        (
            "Infrastructure Cost",
            "Optimize AWS resource utilization",
            ["DevOps", "Performance"],
            85.0
        )
    ]
    
    for title, desc, expected, min_confidence in edge_cases:
        result = predictor.predict(title, desc)
        if isinstance(expected, list):
            assert result["category"] in expected, \
                f"Failed on: {title} - Expected one of {expected}, got {result['category']}"
        else:
            assert result["category"] == expected, \
                f"Failed on: {title} - Expected {expected}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}" 

def test_hybrid_tasks(predictor):
    """Test tasks that span multiple categories with complex interactions"""
    hybrid_cases = [
        # Security + Performance
        (
            "SSL Performance Tuning",
            "Optimize TLS handshake and certificate validation process",
            ["Security", "Performance"],
            85.0
        ),
        # DevOps + Security + Performance
        (
            "Container Security Scan",
            "Implement real-time vulnerability scanning for Docker images with minimal performance impact",
            ["DevOps", "Security", "Performance"],
            85.0
        ),
        # Development + Performance
        (
            "GraphQL Query Optimization",
            "Implement dataloader and connection pooling for GraphQL resolvers",
            ["Development", "Performance"],
            85.0
        ),
        # UI/UX + Performance
        (
            "Animation Performance",
            "Optimize React component animations for 60fps on mobile devices",
            ["UI_UX", "Performance"],
            85.0
        )
    ]
    
    for title, desc, expected_categories, min_confidence in hybrid_cases:
        result = predictor.predict(title, desc)
        assert result["category"] in expected_categories, \
            f"Failed on: {title} - Expected one of {expected_categories}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}"

def test_specialized_scenarios(predictor):
    """Test highly specialized technical tasks"""
    specialized_cases = [
        # Cloud Infrastructure
        (
            "AWS Lambda Cold Start",
            "Reduce function initialization time for serverless endpoints",
            ["Performance", "DevOps"],
            85.0
        ),
        # Database Optimization
        (
            "MongoDB Index Strategy",
            "Implement compound indexes for aggregation pipeline queries",
            ["Performance", "Development"],
            85.0
        ),
        # Security Compliance
        (
            "GDPR Data Handling",
            "Implement data encryption and retention policies for EU compliance",
            ["Security", "Development"],
            85.0
        ),
        # Testing Infrastructure
        (
            "Test Environment Setup",
            "Configure isolated k8s namespace for integration testing",
            ["DevOps", "Testing"],
            85.0
        )
    ]
    
    for title, desc, expected_categories, min_confidence in specialized_cases:
        result = predictor.predict(title, desc)
        assert result["category"] in expected_categories, \
            f"Failed on: {title} - Expected one of {expected_categories}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}" 

def test_technical_specializations(predictor):
    """Test highly technical and specialized tasks"""
    technical_cases = [
        # Frontend Performance
        (
            "React Render Optimization",
            "Implement useMemo and useCallback hooks to prevent unnecessary re-renders in dashboard components",
            ["Performance", "Development"],
            90.0
        ),
        # Backend Performance
        (
            "Database Query Optimization",
            "Implement database materialized views and query denormalization for analytics dashboard",
            ["Performance", "Development"],
            90.0
        ),
        # Cloud Architecture
        (
            "Microservices Communication",
            "Implement service mesh with Istio for inter-service communication and traffic management",
            ["DevOps", "Architecture"],
            90.0
        ),
        # Security Architecture
        (
            "Zero Trust Implementation",
            "Configure identity-aware proxy and implement service-to-service authentication",
            ["Security", "Architecture"],
            90.0
        )
    ]
    
    for title, desc, expected_categories, min_confidence in technical_cases:
        result = predictor.predict(title, desc)
        assert result["category"] in expected_categories, \
            f"Failed on: {title} - Expected one of {expected_categories}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}"

def test_cross_functional_tasks(predictor):
    """Test tasks that require multiple team specialties"""
    cross_functional_cases = [
        # UI/UX + Performance + Security
        (
            "Secure Form Optimization",
            "Implement progressive form validation with CSRF protection and optimal UX",
            ["UI_UX", "Security", "Performance"],
            85.0
        ),
        # DevOps + Security + Compliance
        (
            "SOC2 Pipeline Setup",
            "Configure CI/CD pipeline with security scanning and compliance checks for SOC2",
            ["DevOps", "Security", "Documentation"],
            85.0
        ),
        # Performance + Analytics + Privacy
        (
            "Analytics Performance",
            "Optimize user tracking implementation while ensuring GDPR compliance",
            ["Performance", "Security", "Development"],
            85.0
        )
    ]
    
    for title, desc, expected_categories, min_confidence in cross_functional_cases:
        result = predictor.predict(title, desc)
        assert result["category"] in expected_categories, \
            f"Failed on: {title} - Expected one of {expected_categories}, got {result['category']}"
        assert result["confidence"] >= min_confidence, \
            f"Low confidence on {title}: {result['confidence']}" 