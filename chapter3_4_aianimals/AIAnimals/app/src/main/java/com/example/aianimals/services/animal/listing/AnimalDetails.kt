package com.example.aianimals.services.animal.listing


import com.example.aianimals.core.extension.empty

data class AnimalDetails(
    val id: Int,
    val title: String,
    val poster: String,
    val summary: String,
    val cast: String,
    val director: String,
    val year: Int,
    val trailer: String
) {

    companion object {
        val empty = AnimalDetails(
            0,
            String.empty(),
            String.empty(),
            String.empty(),
            String.empty(),
            String.empty(),
            0,
            String.empty()
        )
    }
}
