


import React, { useState } from 'react';
import Fade from "react-reveal";
import "react-responsive-carousel/lib/styles/carousel.min.css"; // requires a loader
import { Carousel } from 'react-responsive-carousel';
import { tabContents } from '../Data/TabContents.js';



const Download = () => {
    const [selectedTab, setSelectedTab] = useState('windows'); // Default tab is Windows
    const [selectedIndex, setSelectedIndex] = useState(0); // Default index is 0

    const handleIndexChange = (tab) => {
        if (tab === 'windows') {
            setSelectedIndex(0)
        }
        else if (tab === 'macos'){
            setSelectedIndex(1)
        }
        else if (tab === 'linux'){
            setSelectedIndex(2)
        }
        else if (tab === 'raspberry'){ 
            setSelectedIndex(3)
        }
        else {
            setSelectedIndex(tab)
        }
        // console.log(tab);
      };
    

    // Define content for each tab
    

    const imageUrls = Object.values(tabContents).map((tabContent) => tabContent.image);

    const currentTabContent = tabContents[selectedTab];

    // Function to handle tab changes
    const handleTabChange = (index, tab) => {
        setSelectedTab(tab);
        handleIndexChange(tab);
    };

    return (
        <section id='download' className='bg-white'>
            <Fade duration={1000}>
                <div className="flex">
                    {/* Left Column */}
                    <div className="w-1/2 p-4 mt-48 ms-20">
                        {/* Tabs */}

                        <div class="mb-4 border-b border-gray-200 text-3xl dark:border-gray-700">
                            <ul class="flex flex-wrap -mb-px font-medium text-center" id="myTab" role="tablist">
                                <li class="mr-2" role="presentation">
                                    <button className={`inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 ${selectedTab === "windows" ? "text-white bg-gray-700" : "text-gray-600"}`} id="windows-tab" type="button" role="tab" aria-controls="profile" aria-selected="false" onClick={() => handleTabChange(0, 'windows')}>Windows</button>
                                </li>
                                <li class="mr-2" role="presentation">
                                    <button class={`inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 ${selectedTab === "macos" ? "text-white bg-gray-700" : "text-gray-600"}`} id="macos-tab" type="button" role="tab" aria-controls="dashboard" aria-selected="false" onClick={() => handleTabChange(1, 'macos')}>MacOS</button>
                                </li>
                                <li class="mr-2" role="presentation">
                                    <button class={`inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 ${selectedTab === "linux" ? "text-white bg-gray-700" : "text-gray-600"}`} id="linux-tab" type="button" role="tab" aria-controls="settings" aria-selected="false" onClick={() => handleTabChange(2, 'linux')}>Linux</button>
                                </li>
                                <li class="mr-2" role="presentation">
                                    <button class={`inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 ${selectedTab === "raspberry" ? "text-white bg-gray-700" : "text-gray-600"}`} id="linux-tab" type="button" role="tab" aria-controls="settings" aria-selected="false" onClick={() => handleTabChange(3, 'raspberry')}>ARM</button>
                                </li>
                            </ul>
                        </div>


                        {/* Content for the selected tab */}

                        <div className="ms-5">
                            <div class="flex items-center text-5xl">
                                {/* <i className={`${currentTabContent.icon}`} aria-hidden="true"></i> */}
                                <img src='images/icon.png' className='w-16 h-16' alt='IITK FGAuth Icon' />
                                <div class="mx-5">
                                    <h2 class="font-semibold">IITK Fortinet Authenticator</h2>
                                </div>
                            </div>
                            <Fade key={selectedTab} duration={300}>
                                <p className="text-gray-600 my-5">{currentTabContent.heading2}</p>
                                <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-4 px-4 rounded mt-4" onClick={() => window.open(currentTabContent.downloadURL)}>
                                    <i className={`me-3 ${currentTabContent.icon}`}></i>
                                    {currentTabContent.downloadButtonLabel}
                                </button>
                            </Fade>
                        </div>

                    </div>

                    {/* Right Column */}
                    {/* <Slide left key={selectedTab} duration={300}> */}
                        <div className="w-1/2 p-4 items-center justify-center flex">
                            {/* <img src={currentTabContent.image} alt={currentTabContent.heading1} /> */}
                            <Carousel showThumbs={false}
                                showIndicators={false}
                                showStatus={false}
                                selectedItem={selectedIndex}
                                onChange={handleIndexChange}>
                                {imageUrls.map(item => {
                                    // console.log(item);
                                    return (

                                        <div>
                                            <img src={item} alt={currentTabContent.heading1}/>
                                        </div>
                                    )
                                })}
                            </Carousel>
                        </div>
                    {/* </Slide> */}
                </div>
            </Fade>

        </section>

    );
};

export default Download;
