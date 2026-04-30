import { fetchApi } from "./auth";

export interface PersonalizationSettings {
  homepage_layout: Record<string, unknown>[] | null;
  genre_weights: Record<string, number> | null;
  mood_preferences: string[] | null;
  email_digest_enabled: boolean;
  email_digest_frequency: string;
}

export const personalizationApi = {
  getSettings: () => 
    fetchApi<PersonalizationSettings>("/personalization/settings"),
  
  updateGenreWeights: (weights: Record<string, number>) =>
    fetchApi<void>("/personalization/genre-weights", {
      method: "PUT",
      body: JSON.stringify(weights),
    }),
  
  updateHomepageLayout: (layout: Record<string, unknown>[]) =>
    fetchApi<void>("/personalization/homepage-layout", {
      method: "PUT",
      body: JSON.stringify(layout),
    }),
  
  updateMoodPreferences: (moods: string[]) =>
    fetchApi<void>("/personalization/mood-preferences", {
      method: "PUT",
      body: JSON.stringify(moods),
    }),
  
  updateEmailDigest: (enabled: boolean, frequency: string) =>
    fetchApi<void>(`/personalization/email-digest?enabled=${enabled}&frequency=${frequency}`, {
      method: "PUT",
    }),
};
