import React from "react";
import { NavLink } from "react-router-dom";
import { useMobile } from "../../hooks/useMobile";

interface NavItem {
  path: string;
  label: string;
  icon: React.ReactNode;
}

interface BottomNavProps {
  items: NavItem[];
}

export function BottomNav({ items }: BottomNavProps) {
  const { isMobile } = useMobile();

  if (!isMobile) return null;

  return (
    <nav className="bottom-nav">
      {items.map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          className={({ isActive }) =>
            "bottom-nav-item" + (isActive ? " active" : "")
          }
        >
          <span className="bottom-nav-icon">{item.icon}</span>
          <span className="bottom-nav-label">{item.label}</span>
        </NavLink>
      ))}
    </nav>
  );
}

export function BottomSheet({
  isOpen,
  onClose,
  children,
}: {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}) {
  if (!isOpen) return null;

  return (
    <div className="bottom-sheet-overlay" onClick={onClose}>
      <div
        className="bottom-sheet"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="bottom-sheet-handle" />
        {children}
      </div>
    </div>
  );
}
