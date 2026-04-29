import { Link } from 'react-router-dom';
import type { ContinueWatchingItem } from '../api/recommendations';

interface ContinueWatchingProps {
  items: ContinueWatchingItem[];
}

export default function ContinueWatching({ items }: ContinueWatchingProps) {
  if (items.length === 0) return null;

  return (
    <section style={styles.section}>
      <h2 style={styles.title}>Continue Watching</h2>
      <div style={styles.scroll}>
        {items.map((item) => (
          <Link
            key={item.movie.id}
            to={"/movies/" + item.movie.id}
            style={styles.card}
          >
            {item.movie.poster_path ? (
              <img
                src={"http://localhost:8000" + item.movie.poster_path}
                alt={item.movie.title}
                style={styles.poster}
              />
            ) : (
              <div style={styles.posterPlaceholder}>🎬</div>
            )}
            <div style={styles.info}>
              <h3 style={styles.movieTitle}>{item.movie.title}</h3>
              <div style={styles.progressContainer}>
                <div style={styles.progressBar}>
                  <div style={{ ...styles.progressFill, width: item.progress + "%" }} />
                </div>
                <span style={styles.progressText}>{item.progress}%</span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}

const styles: Record<string, React.CSSProperties> = {
  section: { marginBottom: "2rem" },
  title: { fontSize: "1.25rem", marginBottom: "1rem", color: "#333" },
  scroll: {
    display: "flex",
    gap: "1rem",
    overflowX: "auto",
    paddingBottom: "0.5rem",
  },
  card: {
    flex: "0 0 200px",
    background: "white",
    borderRadius: "8px",
    overflow: "hidden",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
    textDecoration: "none",
    color: "inherit",
  },
  poster: { width: "100%", height: "120px", objectFit: "cover" },
  posterPlaceholder: {
    width: "100%",
    height: "120px",
    background: "#e0e0e0",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "2rem",
  },
  info: { padding: "0.75rem" },
  movieTitle: { margin: 0, fontSize: "0.875rem", marginBottom: "0.5rem" },
  progressContainer: { display: "flex", alignItems: "center", gap: "0.5rem" },
  progressBar: {
    flex: 1,
    height: "4px",
    background: "#e0e0e0",
    borderRadius: "2px",
    overflow: "hidden",
  },
  progressFill: { height: "100%", background: "#1976d2" },
  progressText: { fontSize: "0.75rem", color: "#666" },
};
