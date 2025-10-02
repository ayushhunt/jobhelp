import { Job, JobApplication, CandidateProfile } from './job';

export interface CandidateDashboard {
  profile: CandidateProfile;
  stats: {
    totalApplications: number;
    interviewsScheduled: number;
    shortlistedJobs: number;
    profileViews: number;
  };
  recentApplications: JobApplication[];
  recommendedJobs: Job[];
  upcomingInterviews: Interview[];
}

export interface Interview {
  id: string;
  jobApplicationId: string;
  jobApplication: JobApplication;
  scheduledAt: Date;
  duration: number; // in minutes
  type: 'phone' | 'video' | 'in-person' | 'technical';
  location?: string;
  meetingUrl?: string;
  interviewerName: string;
  interviewerEmail: string;
  notes?: string;
  status: 'scheduled' | 'completed' | 'cancelled' | 'rescheduled';
  feedback?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface SavedJob {
  id: string;
  candidateId: string;
  jobId: string;
  job: Job;
  savedAt: Date;
  notes?: string;
}

export interface CandidatePreferences {
  jobAlerts: boolean;
  emailNotifications: boolean;
  profileVisibility: 'public' | 'private' | 'recruiters-only';
  resumeSearchable: boolean;
}

export interface SkillAssessment {
  id: string;
  candidateId: string;
  skill: string;
  level: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  assessmentScore?: number;
  certificationUrl?: string;
  assessedAt: Date;
}

export interface CandidateAnalytics {
  profileViews: {
    total: number;
    thisWeek: number;
    thisMonth: number;
    chartData: { date: string; views: number }[];
  };
  applicationStats: {
    total: number;
    thisWeek: number;
    thisMonth: number;
    statusBreakdown: { status: string; count: number }[];
  };
  searchAppearances: {
    total: number;
    keywords: string[];
  };
}

