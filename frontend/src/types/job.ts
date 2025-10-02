export type JobType = 'full-time' | 'part-time' | 'contract' | 'internship' | 'remote';
export type ExperienceLevel = 'entry' | 'mid' | 'senior' | 'lead' | 'executive';
export type JobStatus = 'draft' | 'active' | 'paused' | 'closed' | 'expired';

export interface Job {
  id: string;
  title: string;
  description: string;
  requirements: string[];
  responsibilities: string[];
  skills: string[];
  jobType: JobType;
  experienceLevel: ExperienceLevel;
  salaryMin?: number;
  salaryMax?: number;
  location: string;
  isRemote: boolean;
  companyId: string;
  company: Company;
  status: JobStatus;
  applicationsCount: number;
  viewsCount: number;
  createdAt: Date;
  updatedAt: Date;
  expiresAt?: Date;
}

export interface Company {
  id: string;
  name: string;
  description: string;
  logo?: string;
  website?: string;
  industry: string;
  size: string;
  location: string;
  foundedYear?: number;
  benefits: string[];
  culture: string[];
  socialLinks: {
    linkedin?: string;
    twitter?: string;
    facebook?: string;
  };
  createdAt: Date;
  updatedAt: Date;
}

export interface JobApplication {
  id: string;
  jobId: string;
  candidateId: string;
  job: Job;
  candidate: CandidateProfile;
  status: ApplicationStatus;
  coverLetter?: string;
  resumeUrl?: string;
  appliedAt: Date;
  updatedAt: Date;
  notes?: string;
  interviewScheduled?: Date;
}

export type ApplicationStatus = 
  | 'applied' 
  | 'under_review' 
  | 'shortlisted' 
  | 'interview_scheduled' 
  | 'interviewed' 
  | 'offer_extended' 
  | 'offer_accepted' 
  | 'offer_declined' 
  | 'rejected' 
  | 'withdrawn';

export interface CandidateProfile {
  id: string;
  userId: string;
  user: User;
  headline: string;
  summary: string;
  skills: string[];
  experience: WorkExperience[];
  education: Education[];
  certifications: Certification[];
  portfolio: PortfolioItem[];
  resumeUrl?: string;
  linkedinUrl?: string;
  githubUrl?: string;
  portfolioUrl?: string;
  desiredJobType: JobType[];
  desiredSalaryMin?: number;
  desiredSalaryMax?: number;
  preferredLocations: string[];
  isOpenToRemote: boolean;
  availability: 'immediate' | '2weeks' | '1month' | '3months';
  createdAt: Date;
  updatedAt: Date;
}

export interface WorkExperience {
  id: string;
  company: string;
  position: string;
  description: string;
  skills: string[];
  startDate: Date;
  endDate?: Date;
  isCurrent: boolean;
}

export interface Education {
  id: string;
  institution: string;
  degree: string;
  fieldOfStudy: string;
  grade?: string;
  startDate: Date;
  endDate?: Date;
  isCurrent: boolean;
}

export interface Certification {
  id: string;
  name: string;
  issuer: string;
  issueDate: Date;
  expiryDate?: Date;
  credentialUrl?: string;
}

export interface PortfolioItem {
  id: string;
  title: string;
  description: string;
  url: string;
  imageUrl?: string;
  technologies: string[];
  category: string;
}

// Import User type
import { User } from './user';

export interface JobFilters {
  keywords?: string;
  location?: string;
  jobType?: JobType[];
  experienceLevel?: ExperienceLevel[];
  salaryMin?: number;
  salaryMax?: number;
  isRemote?: boolean;
  companySize?: string[];
  industry?: string[];
  postedWithin?: 'today' | 'week' | 'month' | 'all';
}

export interface JobSearchResult {
  jobs: Job[];
  total: number;
  page: number;
  pageSize: number;
  filters: JobFilters;
}

