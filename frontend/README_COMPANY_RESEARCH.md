# Company Research Frontend

## Overview

The Company Research Frontend is a modern, responsive Next.js application that provides a comprehensive interface for company research and verification. It integrates with the backend Company Research API to deliver real-time insights about company authenticity, location verification, and comprehensive business intelligence.

## Features

### 🎯 Core Functionality
- **Company Research Form**: Comprehensive form with research depth options
- **Real-time Progress Tracking**: Live progress updates during research
- **Multi-tab Results Display**: Organized view of all research data
- **Quick Company Check**: Fast verification for basic company validation
- **Service Health Monitoring**: Check status of all research services

### 🎨 Design Features
- **Theme-based Setup**: Light/Dark mode with system preference detection
- **Responsive Design**: Mobile-first approach with tablet and desktop optimization
- **Modern UI Components**: Clean, accessible interface following design best practices
- **Smooth Animations**: CSS transitions and micro-interactions
- **Accessibility**: ARIA labels, keyboard navigation, and screen reader support

### 🔧 Technical Features
- **TypeScript**: Full type safety and IntelliSense support
- **Component Architecture**: Modular, reusable components
- **State Management**: React hooks for local state management
- **Error Handling**: Comprehensive error states and user feedback
- **API Integration**: Robust API service with interceptors and error handling

## Architecture

```
src/
├── app/
│   └── company-research/
│       └── page.tsx                 # Main company research page
├── components/
│   └── CompanyResearch/
│       ├── index.ts                  # Component exports
│       ├── CompanyResearchForm.tsx   # Research form component
│       ├── ResearchProgress.tsx      # Progress tracking component
│       └── ResearchResults.tsx       # Results display component
└── services/
    └── companyResearchApi.ts         # API service and types
```

## Components

### CompanyResearchForm
- **Purpose**: Main form for initiating company research
- **Features**: 
  - Company name and domain input
  - Research depth selection (Basic, Standard, Comprehensive)
  - Additional options (employee reviews, financial data, premium access)
  - Form validation and error handling
  - Cost estimation display

### ResearchProgress
- **Purpose**: Real-time progress tracking during research
- **Features**:
  - Progress bar with color-coded status
  - Current task display
  - Completed tasks list
  - Estimated completion time
  - Cancel research functionality

### ResearchResults
- **Purpose**: Comprehensive display of research results
- **Features**:
  - Tabbed interface (Overview, WHOIS, Location, Web Search, Knowledge Graph, AI Analysis)
  - Authenticity scoring display
  - Data source availability indicators
  - Formatted data presentation
  - Risk factors and trust indicators

## API Integration

### CompanyResearchAPIService
The frontend communicates with the backend through a comprehensive API service:

```typescript
// Example usage
const results = await CompanyResearchAPIService.researchCompany({
  company_name: "Microsoft",
  research_depth: "standard",
  user_id: "user123",
  is_premium: false
});
```

### Available Endpoints
- `POST /research` - Perform comprehensive research
- `POST /research/async` - Start asynchronous research
- `GET /research/progress/{id}` - Get research progress
- `DELETE /research/cancel/{id}` - Cancel ongoing research
- `GET /research/cost-estimate` - Get cost estimates
- `GET /research/health` - Check service health
- `GET /research/quick-check` - Quick company verification

## Styling and Theming

### CSS Variables
The application uses CSS custom properties for consistent theming:

```css
:root {
  --background: 0 0% 100%;      /* Light theme background */
  --foreground: 0 0% 0%;        /* Light theme text */
  --card: 0 0% 100%;            /* Card backgrounds */
  --border: 0 0% 89.8%;         /* Border colors */
  --primary: 0 0% 0%;           /* Primary accent color */
  --muted: 0 0% 96.1%;          /* Muted backgrounds */
}

.dark {
  --background: 0 0% 0%;        /* Dark theme background */
  --foreground: 0 0% 100%;      /* Dark theme text */
  --card: 0 0% 0%;              /* Dark card backgrounds */
  --border: 0 0% 14.9%;         /* Dark border colors */
  --primary: 0 0% 100%;         /* Dark primary accent */
  --muted: 0 0% 3.9%;           /* Dark muted backgrounds */
}
```

### Tailwind CSS Classes
The application leverages Tailwind CSS for utility-first styling:

```tsx
// Example component styling
<div className="bg-card border border-border rounded-lg p-6">
  <h3 className="text-lg font-semibold text-card-foreground mb-4">
    Company Information
  </h3>
</div>
```

## Responsive Design

### Breakpoints
- **Mobile**: `< 768px` - Single column layout, collapsible sidebar
- **Tablet**: `768px - 1024px` - Two column grid, expanded sidebar
- **Desktop**: `> 1024px` - Multi-column layout, persistent sidebar

### Mobile-First Approach
```tsx
// Responsive grid example
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Content adapts to screen size */}
</div>
```

## State Management

### Local State
The application uses React hooks for local state management:

```typescript
const [isLoading, setIsLoading] = useState(false);
const [results, setResults] = useState<CompanyResearchResponse | null>(null);
const [progress, setProgress] = useState<ResearchProgressType | null>(null);
const [error, setError] = useState<string | null>(null);
```

### State Flow
1. **Form Submission** → Set loading state
2. **API Call** → Handle response or error
3. **Progress Tracking** → Update progress state
4. **Results Display** → Show final results
5. **Error Handling** → Display error messages

## Error Handling

### API Errors
- Network failures
- Server errors
- Validation errors
- Rate limiting

### User Feedback
- Error messages with dismiss functionality
- Loading states and progress indicators
- Graceful fallbacks for missing data
- Retry mechanisms for failed operations

## Performance Optimizations

### Code Splitting
- Dynamic imports for heavy components
- Route-based code splitting
- Lazy loading of non-critical features

### API Optimization
- Request debouncing
- Response caching
- Progress polling with cleanup
- Connection pooling

### UI Performance
- Memoized components where appropriate
- Efficient re-renders
- Smooth animations with CSS transforms
- Optimized image loading

## Accessibility

### ARIA Support
- Proper heading hierarchy
- Form labels and descriptions
- Button and link accessibility
- Screen reader support

### Keyboard Navigation
- Tab order management
- Keyboard shortcuts
- Focus management
- Escape key handling

### Color and Contrast
- WCAG AA compliance
- High contrast mode support
- Color-blind friendly design
- Theme-aware color schemes

## Testing

### Component Testing
```bash
# Run component tests
npm run test:components

# Test specific component
npm run test CompanyResearchForm
```

### Integration Testing
```bash
# Run integration tests
npm run test:integration

# Test API integration
npm run test:api
```

### E2E Testing
```bash
# Run end-to-end tests
npm run test:e2e

# Test company research flow
npm run test:e2e:research
```

## Development

### Setup
```bash
# Install dependencies
npm install

# Set environment variables
cp .env.example .env.local

# Start development server
npm run dev
```

### Environment Variables
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_DEBUG_MODE=false
```

### Build and Deploy
```bash
# Build for production
npm run build

# Start production server
npm start

# Deploy to Vercel
vercel --prod
```

## Browser Support

### Modern Browsers
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Polyfills
- ES6+ features
- CSS Grid and Flexbox
- Custom properties
- Intersection Observer

## Contributing

### Code Standards
- TypeScript strict mode
- ESLint configuration
- Prettier formatting
- Conventional commits

### Component Guidelines
- Single responsibility principle
- Props interface definition
- Error boundary implementation
- Accessibility compliance

### Testing Requirements
- Unit test coverage > 80%
- Integration test coverage > 70%
- E2E test coverage > 50%
- Accessibility testing

## Future Enhancements

### Planned Features
1. **Advanced Filtering**: Company size, industry, location filters
2. **Export Functionality**: PDF, CSV, JSON export options
3. **Batch Processing**: Multiple company research
4. **Real-time Updates**: WebSocket-based progress updates
5. **Advanced Analytics**: Company comparison and benchmarking

### Technical Improvements
1. **State Management**: Redux Toolkit or Zustand integration
2. **Caching**: React Query for API state management
3. **Performance**: Virtual scrolling for large datasets
4. **Offline Support**: Service worker implementation
5. **PWA Features**: Installable app with offline capabilities

---

*Last updated: August 2024*
*Version: 1.0.0*

