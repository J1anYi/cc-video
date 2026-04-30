import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface TenantSettings {
  logo?: string;
  primaryColor?: string;
  secondaryColor?: string;
  platformName?: string;
}

interface Tenant {
  id: number;
  name: string;
  slug: string;
  plan: string;
  status: string;
  settings?: TenantSettings;
}

interface TenantContextType {
  tenant: Tenant | null;
  tenantId: number | null;
  tenantSettings: TenantSettings;
  isLoading: boolean;
}

const TenantContext = createContext<TenantContextType | undefined>(undefined);

const DEFAULT_SETTINGS: TenantSettings = {
  platformName: 'CC Video',
  primaryColor: '#1976d2',
  secondaryColor: '#dc004e',
};

export function TenantProvider({ children }: { children: ReactNode }) {
  const [tenant, setTenant] = useState<Tenant | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const tenantId = resolveTenantId();
    if (tenantId) {
      fetchTenant(tenantId);
    } else {
      setIsLoading(false);
    }
  }, []);

  const resolveTenantId = (): number | null => {
    const host = window.location.hostname;
    const parts = host.split('.');
    if (parts.length >= 2 && parts[0] !== 'www' && parts[0] !== 'localhost') {
      return null;
    }
    const stored = localStorage.getItem('tenant_id');
    if (stored) {
      return parseInt(stored, 10);
    }
    return null;
  };

  const fetchTenant = async (tenantId: number) => {
    try {
      const response = await fetch('/api/tenants/' + tenantId);
      if (response.ok) {
        const data = await response.json();
        setTenant(data);
      }
    } catch (error) {
      console.error('Failed to fetch tenant:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const tenantSettings: TenantSettings = tenant?.settings 
    ? { ...DEFAULT_SETTINGS, ...JSON.parse(tenant.settings) }
    : DEFAULT_SETTINGS;

  return (
    <TenantContext.Provider value={{
      tenant,
      tenantId: tenant?.id ?? null,
      tenantSettings,
      isLoading,
    }}>
      {children}
    </TenantContext.Provider>
  );
}

export function useTenant() {
  const context = useContext(TenantContext);
  if (context === undefined) {
    throw new Error('useTenant must be used within a TenantProvider');
  }
  return context;
}
