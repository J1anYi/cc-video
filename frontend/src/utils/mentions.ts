export function extractMentions(text: string): string[] {
  const pattern = /@(\w+)/g;
  const matches: string[] = [];
  let match;
  while ((match = pattern.exec(text)) !== null) {
    if (!matches.includes(match[1])) {
      matches.push(match[1]);
    }
  }
  return matches;
}

export function formatMentions(text: string, _getProfileUrl: (username: string) => string): string {
  return text.replace(/@(\w+)/g, '<a href="$1" class="mention">@$1</a>');
}