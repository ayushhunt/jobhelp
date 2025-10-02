'use client'

import React from 'react';
import { ResearchProgress as ResearchProgressType } from '@/services/companyResearchApi';

interface ResearchProgressProps {
  progress: ResearchProgressType;
  onCancel?: () => void;
}

const ResearchProgress: React.FC<ResearchProgressProps> = ({ progress, onCancel }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-600 bg-green-100 dark:bg-green-900/20 dark:text-green-400';
      case 'failed':
        return 'text-red-600 bg-red-100 dark:bg-red-900/20 dark:text-red-400';
      case 'in_progress':
        return 'text-blue-600 bg-blue-100 dark:bg-blue-900/20 dark:text-blue-400';
      case 'partial':
        return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20 dark:text-yellow-400';
      default:
        return 'text-gray-600 bg-gray-100 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return '✅';
      case 'failed':
        return '❌';
      case 'in_progress':
        return '🔄';
      case 'partial':
        return '⚠️';
      default:
        return '⏳';
    }
  };

  const formatStatus = (status: string) => {
    return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'bg-green-500';
    if (progress >= 60) return 'bg-blue-500';
    if (progress >= 40) return 'bg-yellow-500';
    if (progress >= 20) return 'bg-orange-500';
    return 'bg-red-500';
  };

  return (
    <div className="bg-card border border-border rounded-lg p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-card-foreground">
            Research Progress
          </h3>
          <p className="text-sm text-muted-foreground">
            Request ID: {progress.request_id}
          </p>
        </div>
        
        <div className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(progress.status)}`}>
          <span className="mr-2">{getStatusIcon(progress.status)}</span>
          {formatStatus(progress.status)}
        </div>
      </div>

      {/* Company Info */}
      <div className="bg-muted/50 rounded-lg p-4">
        <h4 className="font-medium text-card-foreground mb-2">Company</h4>
        <p className="text-card-foreground">{progress.company_name}</p>
      </div>

      {/* Progress Bar */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-card-foreground">Overall Progress</span>
          <span className="text-muted-foreground">{Math.round(progress.overall_progress)}%</span>
        </div>
        
        <div className="w-full bg-muted rounded-full h-3 overflow-hidden">
          <div
            className={`h-full transition-all duration-500 ease-out ${getProgressColor(progress.overall_progress)}`}
            style={{ width: `${progress.overall_progress}%` }}
          />
        </div>
      </div>

      {/* Current Task */}
      {progress.current_task && (
        <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
          <h4 className="font-medium text-primary mb-2">Current Task</h4>
          <p className="text-primary">{progress.current_task}</p>
        </div>
      )}

      {/* Completed Tasks */}
      {progress.completed_tasks.length > 0 && (
        <div className="space-y-3">
          <h4 className="font-medium text-card-foreground">Completed Tasks</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {progress.completed_tasks.map((task, index) => (
              <div
                key={index}
                className="flex items-center space-x-2 text-sm text-muted-foreground"
              >
                <span className="text-green-500">✓</span>
                <span className="capitalize">{task.replace('_', ' ')}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Estimated Completion */}
      {progress.estimated_completion && (
        <div className="bg-muted/50 rounded-lg p-4">
          <h4 className="font-medium text-card-foreground mb-2">Estimated Completion</h4>
          <p className="text-muted-foreground">
            {new Date(progress.estimated_completion).toLocaleString()}
          </p>
        </div>
      )}

      {/* Last Updated */}
      <div className="text-xs text-muted-foreground text-center">
        Last updated: {new Date(progress.last_updated).toLocaleString()}
      </div>

      {/* Cancel Button */}
      {progress.status === 'in_progress' && onCancel && (
        <div className="flex justify-center">
          <button
            onClick={onCancel}
            className="px-4 py-2 text-sm text-destructive hover:text-destructive/80 border border-destructive/20 hover:border-destructive/40 rounded-md transition-colors"
          >
            Cancel Research
          </button>
        </div>
      )}
    </div>
  );
};

export default ResearchProgress;

