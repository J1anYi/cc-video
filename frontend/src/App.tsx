import { BrowserRouter, Routes, Route, Navigate, Suspense, lazy } from 'react-router-dom';
import { AuthProvider } from './auth/AuthContext';
import ProtectedRoute from './routes/ProtectedRoute';
import { AccessibilityProvider, SkipLinks } from './components/accessibility';
import './App.css';

// Lazy load all route components for better initial load time
const Login = lazy(() => import('./routes/Login'));
const Register = lazy(() => import('./routes/Register'));
const ForgotPassword = lazy(() => import('./routes/ForgotPassword'));
const ResetPassword = lazy(() => import('./routes/ResetPassword'));
const Profile = lazy(() => import('./routes/Profile'));
const Catalog = lazy(() => import('./routes/Catalog'));
const Playback = lazy(() => import('./routes/Playback'));
const History = lazy(() => import('./routes/History'));
const Favorites = lazy(() => import('./routes/Favorites'));
const Feed = lazy(() => import('./routes/Feed'));
const UserProfile = lazy(() => import('./routes/UserProfile'));
const Notifications = lazy(() => import('./routes/Notifications'));
const Watchlists = lazy(() => import('./routes/Watchlists'));
const WatchlistDetail = lazy(() => import('./routes/WatchlistDetail'));
const PublicWatchlists = lazy(() => import('./routes/PublicWatchlists'));
const Analytics = lazy(() => import('./routes/Analytics'));
const AdminMovies = lazy(() => import('./routes/admin/Movies'));
const EditMovie = lazy(() => import('./routes/admin/EditMovie'));
const CreateMovie = lazy(() => import('./routes/admin/CreateMovie'));
const AdminUsers = lazy(() => import('./routes/admin/Users'));
const AdminReports = lazy(() => import('./routes/admin/Reports'));
const AdminMetrics = lazy(() => import('./routes/admin/Metrics'));
const AdminDashboard = lazy(() => import('./routes/admin/Dashboard'));
const SocialAnalyticsPage = lazy(() => import('./routes/SocialAnalytics'));
const RecSettings = lazy(() => import('./routes/RecSettings'));

// Loading component for Suspense fallback
function LoadingSpinner() {
  return (
    <div className="loading-container" role="status" aria-label="Loading">
      <div className="loading-spinner" aria-hidden="true"></div>
      <span className="sr-only">Loading...</span>
    </div>
  );
}

function App() {
  return (
    <AccessibilityProvider>
      <AuthProvider>
        <BrowserRouter>
          <SkipLinks />
          <main id="main-content">
            <Suspense fallback={<LoadingSpinner />}>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/forgot-password" element={<ForgotPassword />} />
                <Route path="/reset-password" element={<ResetPassword />} />
                <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
                <Route path="/analytics" element={<ProtectedRoute><Analytics /></ProtectedRoute>} />
                <Route path="/history" element={<ProtectedRoute><History /></ProtectedRoute>} />
                <Route path="/favorites" element={<ProtectedRoute><Favorites /></ProtectedRoute>} />
                <Route path="/feed" element={<ProtectedRoute><Feed /></ProtectedRoute>} />
                <Route path="/notifications" element={<ProtectedRoute><Notifications /></ProtectedRoute>} />
                <Route path="/watchlists" element={<ProtectedRoute><Watchlists /></ProtectedRoute>} />
                <Route path="/watchlists/:id" element={<ProtectedRoute><WatchlistDetail /></ProtectedRoute>} />
                <Route path="/discover/watchlists" element={<ProtectedRoute><PublicWatchlists /></ProtectedRoute>} />
                <Route path="/users/:userId" element={<ProtectedRoute><UserProfile /></ProtectedRoute>} />
                <Route path="/movies" element={<ProtectedRoute><Catalog /></ProtectedRoute>} />
                <Route path="/movies/:id" element={<ProtectedRoute><Playback /></ProtectedRoute>} />
                <Route path="/admin/movies" element={<ProtectedRoute requireAdmin><AdminMovies /></ProtectedRoute>} />
                <Route path="/admin/movies/new" element={<ProtectedRoute requireAdmin><CreateMovie /></ProtectedRoute>} />
                <Route path="/admin/movies/:id" element={<ProtectedRoute requireAdmin><EditMovie /></ProtectedRoute>} />
                <Route path="/admin/users" element={<ProtectedRoute requireAdmin><AdminUsers /></ProtectedRoute>} />
                <Route path="/admin/reports" element={<ProtectedRoute requireAdmin><AdminReports /></ProtectedRoute>} />
                <Route path="/admin/metrics" element={<ProtectedRoute requireAdmin><AdminMetrics /></ProtectedRoute>} />
                <Route path="/admin/dashboard" element={<ProtectedRoute requireAdmin><AdminDashboard /></ProtectedRoute>} />
                <Route path="/social" element={<ProtectedRoute><SocialAnalyticsPage /></ProtectedRoute>} />
                <Route path="/settings/recommendations" element={<ProtectedRoute><RecSettings /></ProtectedRoute>} />
                <Route path="/" element={<Navigate to="/movies" replace />} />
                <Route path="*" element={<Navigate to="/movies" replace />} />
              </Routes>
            </Suspense>
          </main>
        </BrowserRouter>
      </AuthProvider>
    </AccessibilityProvider>
  );
}

export default App;
