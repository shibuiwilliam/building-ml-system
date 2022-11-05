package com.example.aianimals.repository.animal.source.local

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.aianimals.middleware.Utils

@Entity(tableName = "animals")
data class Animal @JvmOverloads constructor(
    @PrimaryKey @ColumnInfo(name = "id") var id: String = Utils.generateUUID(),
    @ColumnInfo(name = "name") var name: String = "",
    @ColumnInfo(name = "description") var description: String = "",
    @ColumnInfo(name = "like") var like: Int = 0,
    @ColumnInfo(name = "photoUrl") var photoUrl: String = "https://www.anicom-sompo.co.jp/nekonoshiori/wp-content/uploads/2018/12/724-2.jpg",
    @ColumnInfo(name = "created_at") var created_at: String = ""
)
