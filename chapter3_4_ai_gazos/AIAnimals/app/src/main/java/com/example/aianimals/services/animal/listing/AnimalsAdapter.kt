package com.example.aianimals.services.animal.listing

import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.aianimals.R
import com.example.aianimals.core.extension.inflate
import com.example.aianimals.core.extension.loadFromUrl
import com.example.aianimals.core.navigation.Navigator
import kotlinx.android.synthetic.main.row_animal.view.*
import javax.inject.Inject
import kotlin.properties.Delegates

class AnimalsAdapter
@Inject constructor() : RecyclerView.Adapter<AnimalsAdapter.ViewHolder>() {

    internal var collection: List<AnimalView> by Delegates.observable(emptyList()) { _, _, _ ->
        notifyDataSetChanged()
    }

    internal var clickListener: (AnimalView, Navigator.Extras) -> Unit = { _, _ -> }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        ViewHolder(parent.inflate(R.layout.row_animal))

    override fun onBindViewHolder(viewHolder: ViewHolder, position: Int) =
        viewHolder.bind(collection[position], clickListener)

    override fun getItemCount() = collection.size

    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        fun bind(animalView: AnimalView, clickListener: (AnimalView, Navigator.Extras) -> Unit) {
            itemView.animalPoster.loadFromUrl(animalView.poster)
            itemView.setOnClickListener {
                clickListener(
                    animalView,
                    Navigator.Extras(itemView.animalPoster)
                )
            }
        }
    }
}
