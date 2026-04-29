import { Link } from 'react-router-dom';
import type { RecommendedMovie } from '../api/recommendations';

interface RecommendationsProps {
  items: RecommendedMovie[];
}

export default function Recommendations({ items }: RecommendationsProps) {
  if (items.length === 0) return null;

  return (
    <section style={styles.section}>
      <h2 style={styles.title}>Recommended for You</h2>
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
              <span style={styles.reason}>{item.reason}</span>
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
  movieTitle: { margin: 0, fontSize: "0.875rem", marginBottom: "0.25rem" },
  reason: { fontSize: "0.75rem", color: "#666" },
};
