/** Image optimization utilities */

interface ImageOptions {
  src: string;
  width?: number;
  height?: number;
  quality?: number;
  format?: 'webp' | 'avif' | 'jpeg' | 'png';
}

export const imageOptimization = {
  /** Generate optimized image URL with parameters */
  getOptimizedUrl(options: ImageOptions): string {
    const { src, width, height, quality = 80, format } = options;
    
    // If already a data URL or external, return as-is
    if (src.startsWith('data:') || src.startsWith('http')) {
      return src;
    }

    // Build query parameters
    const params = new URLSearchParams();
    if (width) params.set('w', width.toString());
    if (height) params.set('h', height.toString());
    if (quality !== 80) params.set('q', quality.toString());
    if (format) params.set('f', format);

    const queryString = params.toString();
    return queryString ? `${src}?${queryString}` : src;
  },

  /** Generate srcset for responsive images */
  getSrcSet(src: string, sizes: number[]): string {
    return sizes
      .map((size) => `${this.getOptimizedUrl({ src, width: size })} ${size}w`)
      .join(', ');
  },

  /** Lazy load image observer */
  createLazyLoadObserver(): IntersectionObserver | null {
    if (typeof IntersectionObserver === 'undefined') {
      return null;
    }

    return new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const img = entry.target as HTMLImageElement;
            const dataSrc = img.getAttribute('data-src');
            if (dataSrc) {
              img.src = dataSrc;
              img.removeAttribute('data-src');
            }
          }
        });
      },
      { rootMargin: '50px' }
    );
  },

  /** Preload critical image */
  preloadImage(src: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve();
      img.onerror = reject;
      img.src = src;
    });
  },

  /** Check if WebP is supported */
  async supportsWebP(): Promise<boolean> {
    if (typeof document === 'undefined') return false;
    
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 1;
    return canvas.toDataURL('image/webp').startsWith('data:image/webp');
  },

  /** Check if AVIF is supported */
  async supportsAVIF(): Promise<boolean> {
    if (typeof document === 'undefined') return false;
    
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 1;
    return canvas.toDataURL('image/avif').startsWith('data:image/avif');
  },
};

export default imageOptimization;
