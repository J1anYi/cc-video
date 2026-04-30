export interface HDRInfo {
  isSupported: boolean;
  hasHDRDisplay: boolean;
  preferredHDR: boolean;
}

export function detectHDRCapability(): HDRInfo {
  const result: HDRInfo = {
    isSupported: false,
    hasHDRDisplay: false,
    preferredHDR: true
  };

  if (typeof window === "undefined") return result;

  const savedPreference = localStorage.getItem("hdrPreference");
  if (savedPreference !== null) {
    result.preferredHDR = savedPreference === "true";
  }

  const mediaCapabilities = (navigator as any).mediaCapabilities;
  if (mediaCapabilities) {
    result.isSupported = true;
  }

  const screen = window.screen as any;
  if (screen && screen.colorDepth >= 30) {
    result.hasHDRDisplay = true;
  }

  return result;
}

export function setHDRPreference(enabled: boolean): void {
  localStorage.setItem("hdrPreference", String(enabled));
}

export function getHDRPreference(): boolean {
  const saved = localStorage.getItem("hdrPreference");
  return saved !== null ? saved === "true" : true;
}
