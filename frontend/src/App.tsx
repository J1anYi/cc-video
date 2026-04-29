import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './auth/AuthContext';
import ProtectedRoute from './routes/ProtectedRoute';
import Login from './routes/Login';
import Register from './routes/Register';
import Catalog from './routes/Catalog';
import Playback from './routes/Playback';
import AdminMovies from './routes/admin/Movies';
import EditMovie from './routes/admin/EditMovie';
import CreateMovie from './routes/admin/CreateMovie';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/movies"
            element={
              <ProtectedRoute>
                <Catalog />
              </ProtectedRoute>
            }
          />
          <Route
            path="/movies/:id"
            element={
              <ProtectedRoute>
                <Playback />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/movies"
            element={
              <ProtectedRoute requireAdmin>
                <AdminMovies />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/movies/new"
            element={
              <ProtectedRoute requireAdmin>
                <CreateMovie />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/movies/:id"
            element={
              <ProtectedRoute requireAdmin>
                <EditMovie />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<Navigate to="/movies" replace />} />
          <Route path="*" element={<Navigate to="/movies" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
