package com.example.aianimals.middleware

import java.util.*

object Utils {
    fun generateUUID(): String {
        return UUID.randomUUID().toString().replace("-", "")
    }
}