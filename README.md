<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email
-->





<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/nadavleh/Chess_AI">
  </a>

  <h3 align="center">Fishyfish</h3>

  <p align="center">
    This is simple python chess program written with pygame for the GUI. The chess AI uses minimax with alpha-beta prunning
    <br />
    <a href="https://github.com/nadavleh/Chess_AI"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/nadavleh/Chess_AI">View Demo</a>
    ·
    <a href="https://github.com/nadavleh/Chess_AI/issues">Report Bug</a>
    ·
    <a href="https://github.com/nadavleh/Chess_AI/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Prerequisites](#prerequisites)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/nadavleh/Chess_AI/blob/master/images/screenshot.png)

As seen in the image, this project uses the pygmae module inorder to implement a simple chess GUI, in which you play as white against the cumputer which utilizes the minimax algorithm, supplemented by alpha-beta pruning to reduce the effective branching factor. The GUI features "Last move" and "possible piece moves" highlighting in green and yellow respectively. Much of the GUI is based upon the following [Youtube playlist] (https://www.youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_), however you may encounter some critical differences.

### Built With

* [pygame](https://www.pygame.org/docs/)
* [Python 3.7.1](https://www.python.org/downloads/release/python-371/)





## Prerequisites

Just install pygame 1.9.6:
              pip install pygame==1.9.6


## Usage

Simply download the repository and run the ChessMain().py file. You will play as white, against the minimax algorithm with alpha-beta prunning. The current depth of search is 3 layers down the game tree, however the depth can be changed easily by searching for "depth" in ChessMain().py. You'll find this parameter inside the line that calls the function alphaBeta(). You can set this value to any integer greater than zero (at zero depth this function returns only the current board evaluation and thus there's no "best move" to take. Consequently, The program will crash as its trying to make a move of type "None")


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
Project Link: [https://github.com/nadavleh/Chess_AI](https://github.com/nadavleh/Chess_AI)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/nadavleh/repo.svg?style=flat-square
[forks-shield]: https://img.shields.io/github/forks/nadavleh/repo.svg?style=flat-square
[forks-url]: https://github.com/nadavleh/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/nadavleh/repo.svg?style=flat-square
[stars-url]: https://github.com/nadavleh/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/nadavleh/repo.svg?style=flat-square
[issues-url]: https://github.com/nadavleh/repo/issues
[license-shield]: https://img.shields.io/github/license/nadavleh/repo.svg?style=flat-square
[product-screenshot]: https://github.com/nadavleh/Chess_AI/blob/master/images/screenshot.png

