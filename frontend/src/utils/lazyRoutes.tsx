/** Lazy loading utilities for route components */
import React, { Suspense, ComponentType } from 'react';

interface LazyOptions {
  fallback?: React.ReactNode;
}

/** Create lazy loaded component with Suspense */
export function lazyLoad(
  importFn: () => Promise<{ default: ComponentType<unknown> }>,
  options: LazyOptions = {}
) {
  const LazyComponent = React.lazy(importFn);
  
  return (props: Record<string, unknown> = {}) => (
    <Suspense fallback={options.fallback || <div>Loading...</div>}>
      <LazyComponent {...props} />
    </Suspense>
  );
}

/** Preload a lazy component */
export function preload(
  importFn: () => Promise<{ default: ComponentType<unknown> }>
): void {
  importFn();
}

/** Default loading fallback component */
export const LoadingFallback: React.FC = () => (
  <div className="flex items-center justify-center min-h-[200px]">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
  </div>
);

export default { lazyLoad, preload, LoadingFallback };
