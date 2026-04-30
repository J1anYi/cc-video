package com.ccvideo.sdk

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

data class Movie(
    val id: Int,
    val title: String,
    val description: String,
    val poster_url: String,
    val backdrop_url: String,
    val video_url: String,
    val duration: Int,
    val release_year: Int,
    val rating: Double,
    val genres: List<String>
)

interface CCVideoApi {
    @GET("movies")
    suspend fun getMovies(): List<Movie>
    
    @GET("movies/{id}")
    suspend fun getMovie(@Path("id") id: Int): Movie
    
    @GET("movies/search")
    suspend fun searchMovies(@Query("q") query: String): List<Movie>
}

class CCVideoClient private constructor(
    private val api: CCVideoApi,
    private var accessToken: String? = null
) {
    companion object {
        private var instance: CCVideoClient? = null
        
        fun getInstance(baseUrl: String = "http://localhost:8000/api/v1/"): CCVideoClient {
            return instance ?: synchronized(this) {
                instance ?: CCVideoClient(baseUrl).also { instance = it }
            }
        }
    }
    
    private constructor(baseUrl: String) : this(
        Retrofit.Builder()
            .baseUrl(baseUrl)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(CCVideoApi::class.java)
    )
    
    fun setAccessToken(token: String) {
        this.accessToken = token
    }
    
    suspend fun getMovies(): Result<List<Movie>> = try {
        Result.success(api.getMovies())
    } catch (e: Exception) {
        Result.failure(e)
    }
    
    suspend fun getMovie(id: Int): Result<Movie> = try {
        Result.success(api.getMovie(id))
    } catch (e: Exception) {
        Result.failure(e)
    }
    
    suspend fun searchMovies(query: String): Result<List<Movie>> = try {
        Result.success(api.searchMovies(query))
    } catch (e: Exception) {
        Result.failure(e)
    }
    
    fun getStreamUrl(movieId: Int): String? {
        return accessToken?.let { 
            "http://localhost:8000/api/v1/movies/$movieId/stream?token=$it" 
        }
    }
}
