import React from 'react';
import PortfolioResearch from './PortfolioResearch';
import { PortfolioData } from '@/services/companyResearchApi';

const PortfolioResearchDemo: React.FC = () => {
  // Sample portfolio data for demonstration
  const samplePortfolioData: PortfolioData = {
    domain: "example-company.com",
    pages: [
      {
        url: "https://example-company.com/portfolio",
        title: "Our Portfolio - Example Company",
        text: "Example Company is a leading technology solutions provider specializing in web development, mobile applications, and cloud infrastructure. We have successfully delivered over 100 projects for clients across various industries including healthcare, finance, and e-commerce.",
        scraped_at: new Date().toISOString()
      },
      {
        url: "https://example-company.com/projects",
        title: "Featured Projects - Example Company",
        text: "Our team has expertise in React, Node.js, Python, AWS, and Docker. We've built scalable applications for Fortune 500 companies and innovative startups alike.",
        scraped_at: new Date().toISOString()
      }
    ],
    raw_text: "Example Company is a leading technology solutions provider specializing in web development, mobile applications, and cloud infrastructure. We have successfully delivered over 100 projects for clients across various industries including healthcare, finance, and e-commerce. Our team has expertise in React, Node.js, Python, AWS, and Docker. We've built scalable applications for Fortune 500 companies and innovative startups alike.",
    portfolio_urls: [
      "https://example-company.com/portfolio",
      "https://example-company.com/projects",
      "https://example-company.com/case-studies"
    ],
    technologies: [
      "React", "Node.js", "Python", "AWS", "Docker", "TypeScript", "MongoDB", "PostgreSQL"
    ],
    industries: [
      "Healthcare", "Finance", "E-commerce", "Technology", "Startups"
    ],
    projects: [
      "E-commerce platform for retail chain",
      "Healthcare management system",
      "Financial analytics dashboard",
      "Mobile app for logistics company"
    ],
    scraped_at: new Date().toISOString(),
    total_pages_scraped: 2,
    total_content_length: 450,
    llm_summary: {
      summary: "Example Company is a technology solutions provider with expertise in web development, mobile applications, and cloud infrastructure. They have delivered over 100 projects across healthcare, finance, and e-commerce industries. Their technology stack includes React, Node.js, Python, AWS, and Docker. They serve both Fortune 500 companies and innovative startups, demonstrating their ability to work with diverse client needs and scale requirements.",
      method: "llm",
      model_used: "gpt-4",
      generated_at: new Date().toISOString()
    },
    nlp_summary: {
      summary: "Example Company provides technology solutions in web development, mobile applications, and cloud infrastructure. They have completed over 100 projects for healthcare, finance, and e-commerce clients. Their technical expertise includes React, Node.js, Python, AWS, and Docker technologies.",
      method: "nlp",
      key_phrases: [
        "technology solutions provider",
        "web development",
        "mobile applications",
        "cloud infrastructure",
        "React Node.js Python",
        "AWS Docker"
      ],
      entities: {
        "ORG": ["Example Company"],
        "TECH": ["React", "Node.js", "Python", "AWS", "Docker"],
        "INDUSTRY": ["Healthcare", "Finance", "E-commerce"]
      },
      techniques_used: ["keybert", "sumy", "spacy"],
      generated_at: new Date().toISOString()
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-card-foreground mb-2">
          Portfolio Research Demo
        </h1>
        <p className="text-muted-foreground">
          This demonstrates the portfolio research functionality with sample data. 
          In a real scenario, this data would come from the backend API.
        </p>
      </div>
      
      <PortfolioResearch portfolioData={samplePortfolioData} />
    </div>
  );
};

export default PortfolioResearchDemo;
