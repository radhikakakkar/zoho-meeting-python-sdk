<div id="top"></div>

<div align="center">
  <a href="https://github.com/radhikakakkar/zoho-meeting-python-sdk">
    <h3 align="center">Zoho Meeting Python SDK</h3>
  </a>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a>
     <ul>
        <li>Getting Environment Variables for the SDK</li>
        <li>Using the Meeting Methods in Your App</li>
        </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

This is a free tool for you to ensure seemless integration with Zoho meeting in any of your apps. You just have to provide

- Client ID
- Client Secret
- Redirect URI
- Auth Grant

The above three values need to be put in your .env file and you are good to go

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

- Python>=3.6

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/radhikakakkar/zoho-meeting-python-sdk
   ```
2. Create and activate virtual environment
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the tool
   ```sh
   cd <cloned repo parent directory>
    python3 setup.py install
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

## Getting Environment Variables for the SDK

1. **Register your account with Zoho and create the client credentials on their [dev console](https://accounts.zoho.com/signin?servicename=AaaServer&context=&serviceurl=https%3A%2F%2Fapi-console.zoho.com%2Flogin)**
   
   ![Zoho API Console](imgs/zoho_api_console_img.png)

2. **Enter your app's redirect URI where asked and then copy `client_id`, `client_secret` to the `.env` file**

   ![Client Details](imgs/zoho_client_details_img.png)

3. **Here is how you can get the auth grant. This is just a one-time thing!**

   [Get Auth Grant](https://www.zoho.com/meeting/api-integration/authentication.html#:~:text=2.-,Get%20An%20Authorization%20Grant,-URL%3A%20https%3A//accounts)

   Make sure you use the correct scopes:
   
   * _ZohoMeeting.meeting.UPDATE_
   * _ZohoMeeting.meeting.READ_
   * _ZohoMeeting.meeting.CREATE_
   * _ZohoMeeting.meeting.DELETE_

4. **Add the above 4 variables in your `.env` and start running!**

## Using the Meeting Methods in Your App

* Scheduling meetings
* Updating meetings
* Deleting meetings
* Get Meeting Recordings 


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Radhika Kakkar - [@radhikakakkar](https://github.com/radhikakakkar) - radhika3273@gmail.com

Project Link: [https://github.com/radhikakakkar/zoho-meeting-python-sdk](https://github.com/radhikakakkar/zoho-meeting-python-sdk)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [Zoho Meeting API docs](https://www.zoho.com/meeting/api-integration.html)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[linkedin-url]: https://linkedin.com/in/radhika-kakkar/
