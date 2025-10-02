import { Job, JobApplication, Company, CandidateProfile } from './job';
import { User } from './user';

export interface RecruiterProfile {
  id: string;
  userId: string;
  user: User;
  companyId: string;
  company: Company;
  position: string;
  department?: string;
  permissions: RecruiterPermission[];
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export type RecruiterPermission = 
  | 'post_jobs'
  | 'edit_jobs'
  | 'delete_jobs'
  | 'view_candidates'
  | 'contact_candidates'
  | 'schedule_interviews'
  | 'manage_applications'
  | 'view_analytics'
  | 'manage_team'
  | 'manage_billing';

export interface RecruiterDashboard {
  profile: RecruiterProfile;
  stats: {
    activeJobs: number;
    totalApplications: number;
    shortlistedCandidates: number;
    interviewsScheduled: number;
    hiredThisMonth: number;
  };
  recentApplications: JobApplication[];
  activeJobs: Job[];
  upcomingInterviews: RecruiterInterview[];
  pipelineOverview: PipelineStage[];
}

export interface RecruiterInterview {
  id: string;
  jobApplicationId: string;
  jobApplication: JobApplication;
  recruiterId: string;
  recruiter: RecruiterProfile;
  scheduledAt: Date;
  duration: number;
  type: 'phone' | 'video' | 'in-person' | 'technical';
  location?: string;
  meetingUrl?: string;
  notes?: string;
  status: 'scheduled' | 'completed' | 'cancelled' | 'rescheduled';
  feedback?: InterviewFeedback;
  createdAt: Date;
  updatedAt: Date;
}

export interface InterviewFeedback {
  rating: number; // 1-5
  technicalSkills: number;
  communication: number;
  culturalFit: number;
  experience: number;
  notes: string;
  recommendation: 'hire' | 'no_hire' | 'maybe';
  nextSteps?: string;
}

export interface PipelineStage {
  stage: 'applied' | 'screening' | 'interview' | 'final_review' | 'offer' | 'hired';
  count: number;
  candidates: CandidateProfile[];
}

export interface JobAnalytics {
  jobId: string;
  job: Job;
  metrics: {
    views: number;
    applications: number;
    conversionRate: number;
    averageTimeToApply: number;
    topSources: { source: string; count: number }[];
  };
  candidateQuality: {
    averageMatchScore: number;
    skillsAlignment: number;
    experienceAlignment: number;
  };
  timeToHire: {
    averageDays: number;
    stageBreakdown: { stage: string; averageDays: number }[];
  };
}

export interface TeamMember {
  id: string;
  userId: string;
  user: User;
  companyId: string;
  role: string;
  permissions: RecruiterPermission[];
  isActive: boolean;
  invitedBy: string;
  joinedAt: Date;
}

export interface BillingInfo {
  companyId: string;
  plan: SubscriptionPlan;
  status: 'active' | 'cancelled' | 'past_due' | 'trialing';
  currentPeriodStart: Date;
  currentPeriodEnd: Date;
  usage: {
    jobPostings: number;
    candidateContacts: number;
    teamMembers: number;
  };
  limits: {
    jobPostings: number;
    candidateContacts: number;
    teamMembers: number;
  };
}

export interface SubscriptionPlan {
  id: string;
  name: string;
  price: number;
  interval: 'month' | 'year';
  features: string[];
  limits: {
    jobPostings: number;
    candidateContacts: number;
    teamMembers: number;
  };
}

export interface CandidateSearch {
  keywords?: string;
  location?: string;
  skills?: string[];
  experience?: string;
  education?: string;
  availability?: string;
  salaryRange?: { min: number; max: number };
}

export interface SearchResult {
  candidates: CandidateProfile[];
  total: number;
  page: number;
  pageSize: number;
  filters: CandidateSearch;
}

