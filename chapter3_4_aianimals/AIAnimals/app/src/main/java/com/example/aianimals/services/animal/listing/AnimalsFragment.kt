package com.example.aianimals.services.animal.listing

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.annotation.StringRes
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.StaggeredGridLayoutManager
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.example.aianimals.R
import com.example.aianimals.core.exception.Failure
import com.example.aianimals.core.extension.failure
import com.example.aianimals.core.extension.invisible
import com.example.aianimals.core.extension.observe
import com.example.aianimals.core.extension.visible
import com.example.aianimals.core.navigation.Navigator
import com.example.aianimals.core.platform.BaseFragment
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.android.synthetic.main.fragment_animals.*
import javax.inject.Inject


@AndroidEntryPoint
class AnimalsFragment : BaseFragment() {

    @Inject
    lateinit var navigator: Navigator

    @Inject
    lateinit var animalsAdapter: AnimalsAdapter

    private val animalsViewModel: AnimalsViewModel by viewModels()

    lateinit var swipeContainer: SwipeRefreshLayout

    override fun layoutId() = R.layout.fragment_animals

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        with(animalsViewModel) {
            observe(animals, ::renderAnimalsList)
            failure(failure, ::handleFailure)
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        val view: View = inflater.inflate(R.layout.fragment_animals, container, false)
        swipeContainer = view.findViewById<View>(R.id.swipeContainer) as SwipeRefreshLayout

        swipeContainer.setColorSchemeResources(
            android.R.color.holo_blue_bright,
            android.R.color.holo_green_light,
            android.R.color.holo_orange_light,
            android.R.color.holo_red_light
        )
        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        initializeView()
        loadAnimalsList()
        swipeContainer.setOnRefreshListener {
            refresh()
        }
    }

    private fun initializeView() {
        animalList.layoutManager =
            StaggeredGridLayoutManager(3, StaggeredGridLayoutManager.VERTICAL)
        animalList.adapter = animalsAdapter
        animalsAdapter.clickListener = { animal, navigationExtras ->
            navigator.showAnimalDetails(requireActivity(), animal, navigationExtras)
        }
    }

    private fun loadAnimalsList() {
        emptyView.invisible()
        animalList.visible()
        showProgress()
        animalsViewModel.loadAnimals()
    }

    private fun refresh() {
        swipeContainer.isRefreshing = true
        loadAnimalsList()
        swipeContainer.isRefreshing = false
    }

    private fun renderAnimalsList(animals: List<AnimalView>?) {
        animalsAdapter.collection = animals.orEmpty()
        hideProgress()
    }

    private fun handleFailure(failure: Failure?) {
        when (failure) {
            is Failure.NetworkConnection -> renderFailure(R.string.failure_network_connection)
            is Failure.ServerError -> renderFailure(R.string.failure_server_error)
            is AnimalFailure.ListNotAvailable -> renderFailure(R.string.failure_animals_list_unavailable)
            else -> renderFailure(R.string.failure_server_error)
        }
    }

    private fun renderFailure(@StringRes message: Int) {
        animalList.invisible()
        emptyView.visible()
        hideProgress()
        notifyWithAction(message, R.string.action_refresh, ::loadAnimalsList)
    }
}
