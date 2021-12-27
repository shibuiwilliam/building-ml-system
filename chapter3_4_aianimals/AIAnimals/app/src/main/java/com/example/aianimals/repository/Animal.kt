package com.example.aianimals.repository

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey


@Entity(tableName = "animals")
data class Animal @JvmOverloads constructor(
    @PrimaryKey @ColumnInfo(name = "id") var id: Int = -1,
    @ColumnInfo var name: String = "",
    @ColumnInfo var price: Int = -1,
    @ColumnInfo var date: String = ""
) {
}
