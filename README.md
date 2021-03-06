<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage Examples</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This Pathfinding Algorithm Visualizer does exactly what it sounds like it does - visualizes algorithms. This desktop application utilizes an unweighted and undirected grid as the graph that the algorithms will traverse. Click anywhere to place the start node, and click a second time to place the end node. After the start and end nodes have been placed, clicking will create a "wall" node (a node that is not traversable by the algorithms). Chose from the dropdown to select an algorithm, press start, and watch the magic happen. As the algorithm traverses the grid, open nodes are green, closed nodes are blue, and the shortest path nodes are purple. Clicking the "Show Heuristic" button will add the algorithm's heuristic to the visualization. If the algorithm has no heuristic - like BFS - it will not be shown. Finally, the application includes an 'Analytics' tab. After each run, this menu will be updated with the type of algorithm, nodes searched, and Nodes seen from the previous run.

### Built With

* Python
* [PyGame](http://pygame-gui.readthedocs.io)
* [PyGame GUI](https://pygame-gui.readthedocs.io/en/latest/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.


### Installation 

(These are Mac Commands, but the general steps still apply for Microsoft devices)

1. Clone the repo
   ```
   git clone https://github.com/HenryQuillin/pathfinding-algorithm-visualizer
   ```
2. Run setup.py 
   ```
   sudo python3 setup.py install
   ```
6. Wait for the build folder to appear 
8. Run 'main.py'
   ```
   python3 main.py
   ``` 


<!-- USAGE EXAMPLES -->
## Usage 
A*
![Screen Shot 2021-04-05 at 1 06 53 PM](screenshots/astar.png)
A*
![Screen Shot 2021-04-05 at 1 06 53 PM](screenshots/astar2.png)
Breadth First Search 
![Screen Shot 2021-04-05 at 1 06 53 PM](screenshots/bfs.png)
Breadth First Search 
![Screen Shot 2021-04-05 at 1 06 53 PM](screenshots/bfs2.png)
Best First Search 
![Screen Shot 2021-04-05 at 1 06 53 PM](screenshots/bestfs.png)


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Henry Quillin - [Personal Website](https://henryquillin.github.io) - [Linkedin](https://www.linkedin.com/in/henry-quillin-014919204/) - henryquillin@gmail.com

Project Link: [https://github.com/github_username/PONG-with-a-twist](https://github.com/HenryQuillin/pathfinding-algorithm-visualizer)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/github_username
