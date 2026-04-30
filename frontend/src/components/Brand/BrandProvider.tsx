import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface BrandingSettings {
  logo_url: string | null;
  favicon_url: string | null;
  primary_color: string;
  secondary_color: string;
  platform_name: string;
  custom_domain: string | null;
}

interface BrandContextType {
  branding: BrandingSettings;
  applyTheme: () => void;
}

const DEFAULT_BRANDING: BrandingSettings = {
  logo_url: null,
  favicon_url: null,
  primary_color: '#1976d2',
  secondary_color: '#dc004e',
  platform_name: 'CC Video',
  custom_domain: null,
};

const BrandContext = createContext<BrandContextType | undefined>(undefined);

export function BrandProvider({ children }: { children: ReactNode }) {
  const [branding, setBranding] = useState<BrandingSettings>(DEFAULT_BRANDING);

  useEffect(() => {
    fetchBranding();
  }, []);

  useEffect(() => {
    applyTheme();
  }, [branding]);

  const fetchBranding = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch('/api/v1/branding/', {
        headers: {
          'Authorization': 'Bearer ' + token,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setBranding({ ...DEFAULT_BRANDING, ...data });
      }
    } catch (error) {
      console.error('Failed to fetch branding:', error);
    }
  };

  const applyTheme = () => {
    const root = document.documentElement;
    root.style.setProperty('--primary-color', branding.primary_color);
    root.style.setProperty('--secondary-color', branding.secondary_color);

    if (branding.platform_name) {
      document.title = branding.platform_name;
    }

    if (branding.favicon_url) {
      const link: HTMLLinkElement = document.querySelector("link[rel*='icon']") || document.createElement('link');
      link.type = 'image/x-icon';
      link.rel = 'shortcut icon';
      link.href = branding.favicon_url;
      document.getElementsByTagName('head')[0].appendChild(link);
    }
  };

  return (
    <BrandContext.Provider value={{ branding, applyTheme }}>
      {children}
    </BrandContext.Provider>
  );
}

export function useBranding() {
  const context = useContext(BrandContext);
  if (context === undefined) {
    throw new Error('useBranding must be used within a BrandProvider');
  }
  return context;
}
