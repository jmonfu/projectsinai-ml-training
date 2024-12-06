import json
from collections import defaultdict
import os

# Create directories if they don't exist
os.makedirs("ml-training/SmartSynch/data", exist_ok=True)

# Initialize data structure with all samples from training_data.json
data = {
    "samples": [
        {
            "title": "Implement user authentication",
            "description": "Create JWT-based authentication system with user login and registration",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Fix API endpoint bug",
            "description": "Debug and fix the user profile endpoint returning 500 error",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Optimize database queries",
            "description": "Improve performance of slow-running SQL queries in the reporting module",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Implement caching layer",
            "description": "Add Redis caching for frequently accessed data endpoints",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Set up CI/CD pipeline",
            "description": "Configure GitHub Actions for automated testing and deployment",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Implement search functionality",
            "description": "Add Elasticsearch integration for full-text search capabilities",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Add unit tests",
            "description": "Write comprehensive unit tests for the user service module",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Implement rate limiting",
            "description": "Add API rate limiting to prevent abuse of public endpoints",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Set up monitoring",
            "description": "Implement Prometheus and Grafana for system monitoring",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Refactor authentication middleware",
            "description": "Clean up and optimize the auth middleware implementation",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Implement WebSocket support",
            "description": "Add real-time communication capabilities using WebSocket protocol",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Set up Docker containers",
            "description": "Containerize application services using Docker and docker-compose",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Implement file upload",
            "description": "Add secure file upload functionality with S3 storage integration",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Add email service",
            "description": "Implement email notification system using SendGrid API",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Optimize image processing",
            "description": "Implement server-side image optimization and compression",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Add data validation",
            "description": "Implement request validation using JSON schema validation",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Set up backup system",
            "description": "Implement automated database backup and recovery system",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Implement SSO",
            "description": "Add Single Sign-On support using OAuth2 protocol",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Add API documentation",
            "description": "Generate API documentation using Swagger/OpenAPI specification",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Implement logging system",
            "description": "Set up centralized logging with ELK stack integration",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Create landing page mockup",
            "description": "Design a modern, responsive landing page for the main website",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Design new logo",
            "description": "Create a minimalist logo that reflects our brand identity",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Update color scheme",
            "description": "Refresh the application's color palette for better accessibility",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Design mobile app UI",
            "description": "Create user interface designs for the iOS and Android apps",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Create icon set",
            "description": "Design consistent icons for the application's main features",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Design email templates",
            "description": "Create responsive HTML email templates for notifications",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Update dashboard layout",
            "description": "Redesign the analytics dashboard for better data visualization",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Create style guide",
            "description": "Develop comprehensive UI/UX style guide for consistency",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Design onboarding flow",
            "description": "Create user onboarding screens and animations",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Update form elements",
            "description": "Redesign form components for better user experience",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Design notification system",
            "description": "Create visual notification system and toast messages",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Create marketing materials",
            "description": "Design social media graphics and promotional content",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Update typography system",
            "description": "Implement new font hierarchy and spacing guidelines",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Design error states",
            "description": "Create visual feedback for various error scenarios",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Create data visualizations",
            "description": "Design charts and graphs for analytics dashboard",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Design mobile navigation",
            "description": "Create responsive navigation menu for mobile devices",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Update loading states",
            "description": "Design skeleton screens and loading animations",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Create illustration system",
            "description": "Design consistent illustrations for empty states",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Design pricing page",
            "description": "Create layout for subscription plans and pricing tiers",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Update dark mode theme",
            "description": "Design dark mode color palette and component states",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Investigate performance issues",
            "description": "Analyze and document system performance bottlenecks",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Research competitor features",
            "description": "Analyze competing products and document key features",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Evaluate new technologies",
            "description": "Research potential new technologies for upcoming features",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Analyze user feedback",
            "description": "Review and categorize user feedback and feature requests",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Research security best practices",
            "description": "Investigate latest security protocols and standards",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Study market trends",
            "description": "Research current market trends and user preferences",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Investigate cloud solutions",
            "description": "Research cloud providers and their service offerings",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Analyze user behavior",
            "description": "Study user interaction patterns and pain points",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Research accessibility standards",
            "description": "Study WCAG guidelines and accessibility requirements",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Investigate testing frameworks",
            "description": "Research and compare different testing methodologies",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Study scalability options",
            "description": "Research scaling strategies for high-traffic systems",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Analyze deployment strategies",
            "description": "Research different deployment and rollback approaches",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Research payment gateways",
            "description": "Compare different payment processing solutions",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Study data migration approaches",
            "description": "Research strategies for large-scale data migration",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Investigate caching solutions",
            "description": "Research different caching technologies and patterns",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Research mobile frameworks",
            "description": "Compare different mobile development frameworks",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Analyze logging solutions",
            "description": "Research centralized logging and monitoring tools",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Study CI/CD tools",
            "description": "Compare different continuous integration platforms",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Research API design patterns",
            "description": "Study RESTful and GraphQL API design approaches",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Investigate ML frameworks",
            "description": "Research machine learning frameworks and libraries",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Weekly team sync",
            "description": "Regular team meeting to discuss progress and blockers",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Client presentation",
            "description": "Present project progress and gather client feedback",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Design review",
            "description": "Review and discuss new design proposals with team",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Sprint retrospective",
            "description": "Team discussion about sprint outcomes and improvements",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Architecture review",
            "description": "Discuss and review system architecture changes",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Stakeholder update",
            "description": "Update meeting with project stakeholders",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Code review session",
            "description": "Team code review and best practices discussion",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Product demo",
            "description": "Demonstrate new features to stakeholders",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Team training",
            "description": "Technical training session for team members",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Project kickoff",
            "description": "Initial meeting to launch new project phase",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Security review",
            "description": "Review security protocols and potential risks",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Performance review",
            "description": "Discuss system performance metrics and improvements",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "User feedback session",
            "description": "Meeting to review and discuss user feedback",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Release planning",
            "description": "Plan upcoming release schedule and features",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Team workshop",
            "description": "Interactive workshop for skill development",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Vendor meeting",
            "description": "Discussion with third-party service providers",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Requirements gathering",
            "description": "Meeting to collect project requirements",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Technical discussion",
            "description": "Deep dive into technical implementation details",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Status update",
            "description": "Regular project status update meeting",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Team brainstorming",
            "description": "Creative session for problem-solving",
            "category": "Meeting",
            "confidence": 1.0
        },
        {
            "title": "Sprint planning",
            "description": "Plan next sprint's tasks and estimate story points",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Roadmap review",
            "description": "Review and update product roadmap",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Resource allocation",
            "description": "Plan team resource allocation for upcoming projects",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Release schedule",
            "description": "Create detailed release timeline and milestones",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Budget planning",
            "description": "Plan and allocate project budget",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Risk assessment",
            "description": "Identify and plan for potential project risks",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Feature prioritization",
            "description": "Prioritize upcoming features and enhancements",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Capacity planning",
            "description": "Plan team capacity for upcoming quarters",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Infrastructure planning",
            "description": "Plan infrastructure upgrades and scaling",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Testing strategy",
            "description": "Plan testing approach for new features",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Documentation planning",
            "description": "Plan documentation updates and improvements",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Security planning",
            "description": "Plan security audits and improvements",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Performance planning",
            "description": "Plan performance optimization initiatives",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Migration planning",
            "description": "Plan data migration strategy and timeline",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Training planning",
            "description": "Plan team training and development activities",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Maintenance planning",
            "description": "Schedule system maintenance and updates",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Integration planning",
            "description": "Plan third-party service integrations",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Deployment planning",
            "description": "Plan deployment strategy for new features",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Backup planning",
            "description": "Plan data backup and recovery procedures",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Monitoring planning",
            "description": "Plan system monitoring and alerting setup",
            "category": "Planning",
            "confidence": 1.0
        },
        {
            "title": "Update documentation design",
            "description": "Improve the layout and structure of our API documentation",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Design system architecture",
            "description": "Create visual diagrams of system components and interactions",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Fix database connection",
            "description": "Debug and resolve intermittent database connectivity issues",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Debug API endpoint",
            "description": "Investigate and fix server errors in the API",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Update documentation design",
            "description": "Improve the layout and structure of our API documentation",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Design system architecture diagrams",
            "description": "Create visual representations of our system components",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Redesign database schema",
            "description": "Create visual layout for improved database structure",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "UI/API integration design",
            "description": "Design interface patterns for API interactions",
            "category": "Design",
            "confidence": 1.0
        },
        {
            "title": "Implement database fixes",
            "description": "Apply patches to resolve database performance issues",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Debug API endpoints",
            "description": "Fix server errors in REST API implementation",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Optimize database queries",
            "description": "Improve performance of slow database operations",
            "category": "Development",
            "confidence": 1.0
        },
        {
            "title": "Research database solutions",
            "description": "Investigate options for database optimization",
            "category": "Research",
            "confidence": 1.0
        },
        {
            "title": "Analyze system performance",
            "description": "Research and document system bottlenecks",
            "category": "Research",
            "confidence": 1.0
        }
    ]
}

# Track unique entries and category counts
seen = set()
category_count = defaultdict(int)
clean_samples = []

# Process samples
for sample in data["samples"]:
    key = (sample["title"].lower(), sample["category"])
    if key not in seen:
        seen.add(key)
        category_count[sample["category"]] += 1
        clean_samples.append(sample)

# Create cleaned data structure
clean_data = {
    "samples": clean_samples
}

# Write cleaned data back to file
with open("ml-training/SmartSynch/data/training_data.json", "w") as f:
    json.dump(clean_data, f, indent=2)

# Print statistics
print("\nCategory distribution after cleanup:")
for category, count in sorted(category_count.items()):
    print(f"{category}: {count} items")
