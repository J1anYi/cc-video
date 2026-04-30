/** Performance monitoring utilities */

interface PerformanceMetrics {
  lcp: number | null;
  fid: number | null;
  cls: number | null;
  ttfb: number | null;
}

export const performanceMonitor = {
  /** Get Core Web Vitals metrics */
  getMetrics(): PerformanceMetrics {
    const metrics: PerformanceMetrics = {
      lcp: null,
      fid: null,
      cls: null,
      ttfb: null,
    };

    if (typeof window === 'undefined' || !window.performance) {
      return metrics;
    }

    // Largest Contentful Paint
    try {
      const lcpEntries = performance.getEntriesByType('largest-contentful-paint');
      if (lcpEntries.length > 0) {
        metrics.lcp = (lcpEntries[lcpEntries.length - 1] as PerformanceEntry & { renderTime: number }).renderTime;
      }
    } catch (e) {
      // LCP not supported
    }

    // First Input Delay
    try {
      const fidEntries = performance.getEntriesByType('first-input');
      if (fidEntries.length > 0) {
        const entry = fidEntries[0] as PerformanceEntry & { processingStart: number; startTime: number };
        metrics.fid = entry.processingStart - entry.startTime;
      }
    } catch (e) {
      // FID not supported
    }

    // Cumulative Layout Shift
    try {
      const clsEntries = performance.getEntriesByType('layout-shift');
      let cls = 0;
      clsEntries.forEach((entry) => {
        const shiftEntry = entry as PerformanceEntry & { hadRecentInput: boolean; value: number };
        if (!shiftEntry.hadRecentInput) {
          cls += shiftEntry.value;
        }
      });
      metrics.cls = cls;
    } catch (e) {
      // CLS not supported
    }

    // Time to First Byte
    try {
      const navigationEntries = performance.getEntriesByType('navigation');
      if (navigationEntries.length > 0) {
        const navEntry = navigationEntries[0] as PerformanceNavigationTiming;
        metrics.ttfb = navEntry.responseStart - navEntry.requestStart;
      }
    } catch (e) {
      // TTFB not supported
    }

    return metrics;
  },

  /** Log performance metrics */
  logMetrics(): void {
    const metrics = this.getMetrics();
    console.log('Core Web Vitals:', {
      LCP: metrics.lcp ? `${metrics.lcp.toFixed(0)}ms` : 'N/A',
      FID: metrics.fid ? `${metrics.fid.toFixed(0)}ms` : 'N/A',
      CLS: metrics.cls ? metrics.cls.toFixed(3) : 'N/A',
      TTFB: metrics.ttfb ? `${metrics.ttfb.toFixed(0)}ms` : 'N/A',
    });
  },

  /** Mark performance timing */
  mark(name: string): void {
    if (typeof performance !== 'undefined') {
      performance.mark(name);
    }
  },

  /** Measure performance between marks */
  measure(name: string, startMark: string, endMark: string): number | null {
    if (typeof performance !== 'undefined') {
      try {
        performance.measure(name, startMark, endMark);
        const entries = performance.getEntriesByName(name, 'measure');
        return entries.length > 0 ? entries[0].duration : null;
      } catch (e) {
        return null;
      }
    }
    return null;
  },
};

export default performanceMonitor;
