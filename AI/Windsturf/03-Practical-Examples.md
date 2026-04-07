# Cascade - Ví Dụ Thực Tế

## 1. Scenario: Refactor Legacy Codebase

### 1.1 Initial Assessment

```
User: "Refactor đoạn code này sang TypeScript và MUI"
[Attached: @/src/components/OldComponent.jsx]
```

**Cascade Actions:**

```typescript
// Step 1: Read và analyze
read_file: @/src/components/OldComponent.jsx
read_file: @/tsconfig.json  // Check TS config
read_file: @/package.json   // Check dependencies

// Step 2: Search patterns
grep_search: "PropTypes"    // Legacy pattern
grep_search: "makeStyles"   // Old MUI pattern

// Step 3: Plan refactor
// - Convert PropTypes → TypeScript interfaces
// - Convert makeStyles → sx prop
// - Update imports
```

### 1.2 Implementation

```typescript
// Before (OldComponent.jsx)
import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles({
  root: { padding: 16 },
  button: { marginTop: 8 }
});

function OldComponent({ title, onClick }) {
  const classes = useStyles();
  return (
    <div className={classes.root}>
      <h1>{title}</h1>
      <button className={classes.button} onClick={onClick}>
        Click
      </button>
    </div>
  );
}

OldComponent.propTypes = {
  title: PropTypes.string.isRequired,
  onClick: PropTypes.func
};

// After (OldComponent.tsx)
import React from 'react';
import { Box, Button, Typography } from '@mui/material';

interface OldComponentProps {
  title: string;
  onClick?: () => void;
}

export function OldComponent({ title, onClick }: OldComponentProps) {
  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h1">{title}</Typography>
      <Button 
        variant="contained" 
        onClick={onClick}
        sx={{ mt: 1 }}
      >
        Click
      </Button>
    </Box>
  );
}
```

### 1.3 Verification

```bash
# Run type check
npx tsc --noEmit

# Run linter
npm run lint

# Run tests
npm test -- OldComponent
```

---

## 2. Scenario: Debug Production Issue

### 2.1 Problem Analysis

```
User: "API call bị lỗi 500, log đây: [paste error log]"
```

**Cascade Investigation:**

```typescript
// Step 1: Locate error source
grep_search: "getUserData"  // Function từ stack trace
code_search: "Find API error handling patterns"

// Step 2: Read relevant code
read_file: @/src/services/api.ts
read_file: @/src/hooks/useUser.ts

// Step 3: Analyze flow
// - Request đi từ component → hook → service
// - Check error handling tại mỗi layer
```

### 2.2 Root Cause Identification

```typescript
// @/src/services/api.ts:45-55
async function getUserData(userId: string) {
  // ❌ Bug: Không handle null userId
  const response = await fetch(`/api/users/${userId}`);
  
  // ❌ Bug: Không check response.ok
  return response.json();
}

// @/src/hooks/useUser.ts:20-30
export function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => getUserData(userId),
    // ❌ Thiếu error handling
  });
}
```

### 2.3 Fix Implementation

```typescript
// @/src/services/api.ts:45-65
async function getUserData(userId: string) {
  // ✅ Validate input
  if (!userId) {
    throw new Error('userId is required');
  }
  
  const response = await fetch(`/api/users/${userId}`);
  
  // ✅ Check response
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || `HTTP ${response.status}`);
  }
  
  return response.json();
}

// @/src/hooks/useUser.ts:20-35
export function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => getUserData(userId),
    // ✅ Proper error handling
    retry: 3,
    retryDelay: 1000,
    // ✅ Disable khi invalid input
    enabled: !!userId,
  });
}
```

---

## 3. Scenario: Feature Implementation

### 3.1 Requirements Analysis

```
User: "Thêm feature export CSV cho data table"
```

**Cascade Planning:**

```markdown
## Implementation Plan:

1. Research:
   - Check current table implementation
   - Find existing export functionality
   - Evaluate CSV libraries

2. Implementation:
   - Add export button to table header
   - Implement CSV generation
   - Handle large datasets

3. Testing:
   - Unit tests cho CSV generation
   - E2E test cho export flow
```

### 3.2 Step-by-Step Execution

```typescript
// Step 1: Explore existing code
code_search: "Find data table components"
read_file: @/src/components/DataTable/index.tsx

// Step 2: Check dependencies
read_file: @/package.json  // Look for csv libraries
grep_search: "download.*csv|export.*file"  // Existing patterns

// Step 3: Implement solution
// @/src/components/DataTable/ExportButton.tsx
import { Button } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';

interface ExportButtonProps {
  data: Record<string, unknown>[];
  filename?: string;
}

export function ExportButton({ data, filename = 'export.csv' }: ExportButtonProps) {
  const handleExport = () => {
    // Convert data to CSV
    const headers = Object.keys(data[0] || {});
    const csvContent = [
      headers.join(','),
      ...data.map(row => 
        headers.map(h => {
          const value = row[h];
          // Escape values with commas/quotes
          const stringValue = String(value ?? '');
          if (stringValue.includes(',') || stringValue.includes('"')) {
            return `"${stringValue.replace(/"/g, '""')}"`;
          }
          return stringValue;
        }).join(',')
      )
    ].join('\n');
    
    // Download
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };
  
  return (
    <Button 
      startIcon={<DownloadIcon />}
      onClick={handleExport}
      variant="outlined"
      size="small"
    >
      Export CSV
    </Button>
  );
}
```

### 3.3 Integration

```typescript
// @/src/components/DataTable/index.tsx:1-50
import { ExportButton } from './ExportButton';

export function DataTable<T extends Record<string, unknown>>({ 
  data, 
  columns,
  title 
}: DataTableProps<T>) {
  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6">{title}</Typography>
        <ExportButton data={data} filename={`${title.toLowerCase().replace(/\s+/g, '_')}.csv`} />
      </Box>
      <Table>...</Table>
    </Box>
  );
}
```

---

## 4. Scenario: Performance Optimization

### 4.1 Issue Detection

```
User: "Page load chậm, cần optimize"
```

**Cascade Analysis:**

```bash
# Step 1: Run build analysis
npm run build
npx webpack-bundle-analyzer dist/static/js/*.js

# Step 2: Check Lighthouse
# - Large bundle size detected (2.5MB)
# - Unused JavaScript: 1.2MB
# - Render-blocking resources
```

### 4.2 Optimization Plan

```markdown
## Optimizations:

1. Code Splitting
   - Lazy load routes
   - Dynamic imports cho heavy components

2. Tree Shaking
   - Fix side-effect imports
   - Remove unused dependencies

3. Asset Optimization
   - Compress images
   - Use WebP format
   - Implement lazy loading images

4. Caching Strategy
   - Service worker cho static assets
   - Memoize expensive calculations
```

### 4.3 Implementation

```typescript
// @/src/App.tsx:1-30
import { lazy, Suspense } from 'react';
import { CircularProgress } from '@mui/material';

// ✅ Lazy load routes
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Reports = lazy(() => import('./pages/Reports'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<CircularProgress />}>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}

// @/src/components/HeavyChart.tsx:1-20
import { lazy } from 'react';

// ✅ Dynamic import cho heavy library
const ChartComponent = lazy(() => import('recharts').then(m => ({ 
  default: m.LineChart 
})));

export function HeavyChart({ data }) {
  const [showChart, setShowChart] = useState(false);
  
  return (
    <div>
      <button onClick={() => setShowChart(true)}>Load Chart</button>
      {showChart && (
        <Suspense fallback={<div>Loading chart...</div>}>
          <ChartComponent data={data} />
        </Suspense>
      )}
    </div>
  );
}
```

### 4.4 Results

```markdown
Before Optimization:
- Initial bundle: 2.5MB
- Page load: 4.2s
- Lighthouse score: 45

After Optimization:
- Initial bundle: 850KB
- Page load: 1.1s  
- Lighthouse score: 92
```

---

## 5. Scenario: Testing Strategy

### 5.1 Test Coverage Analysis

```
User: "Thêm test cho authentication flow"
```

**Cascade Approach:**

```typescript
// Step 1: Explore auth implementation
code_search: "Find authentication related code"
read_file: @/src/services/auth.ts
read_file: @/src/hooks/useAuth.ts

// Step 2: Identify test boundaries
// - Unit: auth service functions
// - Integration: hook with mock service
// - E2E: login → dashboard flow
```

### 5.2 Test Implementation

```typescript
// @/src/services/__tests__/auth.test.ts
import { login, logout, refreshToken } from '../auth';

describe('Auth Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('login', () => {
    it('should store tokens on successful login', async () => {
      const mockResponse = {
        accessToken: 'mock-access',
        refreshToken: 'mock-refresh',
        user: { id: '1', email: 'test@example.com' }
      };
      
      global.fetch = jest.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      });
      
      const result = await login('test@example.com', 'password');
      
      expect(localStorage.setItem).toHaveBeenCalledWith('accessToken', 'mock-access');
      expect(result.user.email).toBe('test@example.com');
    });
    
    it('should throw error on invalid credentials', async () => {
      global.fetch = jest.fn().mockResolvedValue({
        ok: false,
        status: 401,
        json: () => Promise.resolve({ message: 'Invalid credentials' })
      });
      
      await expect(login('test@example.com', 'wrong'))
        .rejects.toThrow('Invalid credentials');
    });
  });
  
  describe('logout', () => {
    it('should clear tokens and call API', async () => {
      localStorage.setItem('refreshToken', 'token');
      
      global.fetch = jest.fn().mockResolvedValue({ ok: true });
      
      await logout();
      
      expect(localStorage.removeItem).toHaveBeenCalledWith('accessToken');
      expect(localStorage.removeItem).toHaveBeenCalledWith('refreshToken');
    });
  });
});

// @/src/hooks/__tests__/useAuth.test.tsx
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuth } from '../useAuth';

const createWrapper = () => {
  const queryClient = new QueryClient();
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

describe('useAuth', () => {
  it('should return authenticated user', async () => {
    const { result } = renderHook(() => useAuth(), {
      wrapper: createWrapper()
    });
    
    await waitFor(() => {
      expect(result.current.user).toBeDefined();
    });
  });
  
  it('should handle login mutation', async () => {
    const { result } = renderHook(() => useAuth(), {
      wrapper: createWrapper()
    });
    
    result.current.login.mutate({ email: 'test@test.com', password: 'pass' });
    
    await waitFor(() => {
      expect(result.current.login.isSuccess).toBe(true);
    });
  });
});
```

---

## 6. Scenario: Code Review Workflow

### 6.1 Setting Up Review Checklist

```yaml
---
description: Code review checklist for PRs
---

## Code Review Checklist

### 1. Functionality
- [ ] Feature works as described
- [ ] Edge cases handled
- [ ] No console errors

### 2. Code Quality
- [ ] Follows project conventions
- [ ] No code duplication
- [ ] Proper error handling
- [ ] Meaningful variable names

### 3. Performance
- [ ] No unnecessary re-renders
- [ ] Efficient data fetching
- [ ] Proper memoization

### 4. Testing
- [ ] Unit tests added/updated
- [ ] Integration tests if needed
- [ ] All tests passing

### 5. Security
- [ ] No hardcoded secrets
- [ ] Input validation
- [ ] XSS prevention

### 6. Documentation
- [ ] JSDoc cho public APIs
- [ ] README updated if needed
- [ ] Changelog updated
```

### 6.2 Using in PR Review

```
User: /code-review

Cascade: ## Code Review Checklist

### 1. Functionality
- [ ] Feature works as described
- [ ] Edge cases handled  
- [ ] No console errors

[Continue checklist...]

User: Check file @/src/components/NewFeature.tsx:1-100

Cascade: ### Review for @/src/components/NewFeature.tsx

**Issues found:**
1. **Line 45**: `useEffect` dependency array thiếu `userId`  
2. **Line 62**: Không handle loading state
3. **Line 78**: Magic number `1000` - nên đặt constant

**Recommendations:**
- Add `isLoading` state
- Extract `POLL_INTERVAL = 1000` constant
- Add cleanup trong useEffect
```

---

## 7. Quick Patterns Reference

### 7.1 Common Refactor Patterns

| Pattern | Before | After |
|---------|--------|-------|
| **Callback → Async/Await** | `fn().then().catch()` | `await fn()` with try/catch |
| **PropTypes → TypeScript** | `Component.propTypes = {}` | `interface Props {}` |
| **Inline Styles → MUI** | `style={{ padding: 16 }}` | `sx={{ p: 2 }}` |
| **Class → Function** | `class X extends Component` | `function X()` with hooks |
| **any → Typed** | `: any` | Proper interface |

### 7.2 Error Handling Patterns

```typescript
// API Layer
try {
  const response = await fetch(url);
  if (!response.ok) {
    throw new ApiError(response.status, await response.json());
  }
  return response.json();
} catch (error) {
  logger.error('API call failed', { url, error });
  throw error;
}

// Component Layer
const { data, error, isLoading } = useQuery(...);

if (isLoading) return <Skeleton />;
if (error) return <ErrorMessage error={error} />;
return <DataView data={data} />;
```
