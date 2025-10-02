export interface ResumeBuilderData {
  personalInfo: {
    firstName: string;
    lastName: string;
    email: string;
    phone: string;
    location: string;
    website?: string;
    linkedin?: string;
    github?: string;
  };
  summary: string;
  experience: ResumeExperience[];
  education: ResumeEducation[];
  skills: ResumeSkill[];
  projects: ResumeProject[];
  certifications: ResumeCertification[];
  languages: ResumeLanguage[];
}

export interface ResumeExperience {
  id: string;
  company: string;
  position: string;
  location: string;
  startDate: string;
  endDate?: string;
  current: boolean;
  description: string;
  achievements: string[];
}

export interface ResumeEducation {
  id: string;
  institution: string;
  degree: string;
  fieldOfStudy: string;
  location: string;
  startDate: string;
  endDate?: string;
  current: boolean;
  gpa?: string;
  honors?: string[];
}

export interface ResumeSkill {
  id: string;
  name: string;
  category: 'technical' | 'soft' | 'language' | 'tool';
  level: 'beginner' | 'intermediate' | 'advanced' | 'expert';
}

export interface ResumeProject {
  id: string;
  name: string;
  description: string;
  technologies: string[];
  url?: string;
  githubUrl?: string;
  startDate: string;
  endDate?: string;
  current: boolean;
}

export interface ResumeCertification {
  id: string;
  name: string;
  issuer: string;
  issueDate: string;
  expiryDate?: string;
  credentialUrl?: string;
}

export interface ResumeLanguage {
  id: string;
  language: string;
  proficiency: 'basic' | 'conversational' | 'fluent' | 'native';
}

export interface ResumeTemplate {
  id: string;
  name: string;
  category: 'modern' | 'classic' | 'creative' | 'minimal' | 'professional';
  previewImage: string;
  isPremium: boolean;
}

export interface CoverLetterData {
  jobTitle: string;
  companyName: string;
  hiringManagerName?: string;
  jobDescription: string;
  candidateName: string;
  candidateEmail: string;
  candidatePhone: string;
  introduction: string;
  bodyParagraphs: string[];
  closing: string;
  template: CoverLetterTemplate;
}

export interface CoverLetterTemplate {
  id: string;
  name: string;
  style: 'formal' | 'creative' | 'modern' | 'traditional';
  previewImage: string;
}

export interface SalaryEstimate {
  jobTitle: string;
  location: string;
  experienceLevel: string;
  skills: string[];
  estimate: {
    min: number;
    max: number;
    median: number;
    currency: string;
  };
  factors: {
    title: number;
    location: number;
    experience: number;
    skills: number;
  };
  marketData: {
    dataPoints: number;
    lastUpdated: Date;
    sources: string[];
  };
  recommendations: string[];
}

export interface InterviewQuestion {
  id: string;
  question: string;
  category: 'behavioral' | 'technical' | 'situational' | 'company-specific';
  difficulty: 'easy' | 'medium' | 'hard';
  sampleAnswer?: string;
  tips: string[];
  followUpQuestions?: string[];
}

export interface InterviewSession {
  id: string;
  jobTitle: string;
  companyName?: string;
  duration: number;
  questions: InterviewQuestion[];
  userAnswers: { questionId: string; answer: string; rating?: number }[];
  feedback: {
    overallScore: number;
    strengths: string[];
    improvements: string[];
    recommendations: string[];
  };
  completedAt?: Date;
}

export interface CareerPath {
  id: string;
  title: string;
  description: string;
  currentRole: string;
  targetRole: string;
  timeframe: string;
  steps: CareerStep[];
  requiredSkills: string[];
  averageSalary: {
    current: number;
    target: number;
  };
  marketDemand: 'low' | 'medium' | 'high';
}

export interface CareerStep {
  id: string;
  title: string;
  description: string;
  duration: string;
  requirements: string[];
  resources: CareerResource[];
  completed?: boolean;
}

export interface CareerResource {
  id: string;
  title: string;
  type: 'course' | 'book' | 'certification' | 'project' | 'networking';
  url?: string;
  provider: string;
  cost: 'free' | 'paid';
  rating?: number;
}

export interface ToolUsageAnalytics {
  toolName: string;
  usageCount: number;
  lastUsed: Date;
  averageSessionDuration: number;
  completionRate: number;
}

