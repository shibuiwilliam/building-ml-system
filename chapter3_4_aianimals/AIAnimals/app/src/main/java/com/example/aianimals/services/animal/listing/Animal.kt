package com.example.aianimals.services.animal.listing


import com.example.aianimals.core.extension.empty

data class Animal(val id: Int, val poster: String) {

    companion object {
        val empty = Animal(0, String.empty())
    }
}
