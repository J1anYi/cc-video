import Foundation
import Alamofire

public class CCVideoClient {
    private let baseURL: String
    private var accessToken: String?
    
    public init(baseURL: String = "http://localhost:8000/api/v1") {
        self.baseURL = baseURL
    }
    
    public func setAccessToken(_ token: String) {
        self.accessToken = token
    }
    
    public func getMovies(completion: @escaping (Result<[Movie], Error>) -> Void) {
        AF.request("\(baseURL)/movies")
            .validate()
            .responseDecodable(of: [Movie].self) { response in
                switch response.result {
                case .success(let movies): completion(.success(movies))
                case .failure(let error): completion(.failure(error))
                }
            }
    }
    
    public func getMovie(id: Int, completion: @escaping (Result<Movie, Error>) -> Void) {
        AF.request("\(baseURL)/movies/\(id)")
            .validate()
            .responseDecodable(of: Movie.self) { response in
                switch response.result {
                case .success(let movie): completion(.success(movie))
                case .failure(let error): completion(.failure(error))
                }
            }
    }
    
    public func searchMovies(query: String, completion: @escaping (Result<[Movie], Error>) -> Void) {
        AF.request("\(baseURL)/movies/search", parameters: ["q": query])
            .validate()
            .responseDecodable(of: [Movie].self) { response in
                switch response.result {
                case .success(let movies): completion(.success(movies))
                case .failure(let error): completion(.failure(error))
                }
            }
    }
}

public struct Movie: Codable {
    public let id: Int
    public let title: String
    public let description: String
    public let poster_url: String
    public let backdrop_url: String
    public let video_url: String
    public let duration: Int
    public let release_year: Int
    public let rating: Double
    public let genres: [String]
}
