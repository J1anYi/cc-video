# CC Video Platform SDK

Multi-platform SDK for integrating CC Video into your applications.

## Installation

### iOS (Swift Package Manager)
```swift
dependencies: [
    .package(url: "https://github.com/ccvideo/ios-sdk.git", from: "1.0.0")
]
```

### Android (Gradle)
```gradle
implementation 'com.ccvideo:sdk:1.0.0'
```

### Web (npm)
```bash
npm install @ccvideo/sdk
```

## Quick Start

### iOS
```swift
import CCVideoSDK

let client = CCVideoClient()
client.setAccessToken("your-token")

client.getMovies { result in
    switch result {
    case .success(let movies):
        print(movies)
    case .failure(let error):
        print(error)
    }
}
```

### Android
```kotlin
val client = CCVideoClient.getInstance()
client.setAccessToken("your-token")

val movies = client.getMovies().getOrNull()
```

### Web
```typescript
import { CCVideoClient } from '@ccvideo/sdk';

const client = new CCVideoClient({ accessToken: 'your-token' });
const movies = await client.getMovies();
```

## API Reference

### CCVideoClient

| Method | Description |
|--------|-------------|
| setAccessToken(token) | Set authentication token |
| getMovies() | Get all movies |
| getMovie(id) | Get single movie |
| searchMovies(query) | Search movies |
| getStreamUrl(movieId) | Get video stream URL |

## Versioning

We follow Semantic Versioning.

- MAJOR: Breaking API changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes

## License

MIT License
