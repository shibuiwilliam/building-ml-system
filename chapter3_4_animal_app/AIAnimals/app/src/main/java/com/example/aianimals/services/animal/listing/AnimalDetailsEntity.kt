package com.example.aianimals.services.animal.listing

import com.example.aianimals.core.extension.empty


data class AnimalDetailsEntity(
    private val id: Int,
    private val title: String,
    private val poster: String,
    private val summary: String,
    private val cast: String,
    private val director: String,
    private val year: Int,
    private val trailer: String
) {

    companion object {
        val empty = AnimalDetailsEntity(
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

    fun toAnimalDetails() = AnimalDetails(
        id,
        title,
        poster,
        summary,
        cast,
        director,
        year,
        trailer
    )
}
