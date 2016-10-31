### Aims & background material (student)

This project aims to implement a speed reporting system using license plate recognition techniques, applied to a camera input. The system should be able to extract license plates from incoming video, communicate it with neighbouring systems and figure out the average speed a vehicle must have been travelling at using Speed = Distance / Time. Vehicles over the speed limit should then be reported online using social media or similar platforms.

The system should be distributed (the performance of the system should be proportional to the number of deployed systems), and be decentralized (there should not be a centralized server that the systems report to, based on privacy and security concerns).

Background material and literature reviews will be split across technical (license plate recognition algorithms and networking protocols), business-focused (feasibility study, surveys), and non-technical literature (public records, newspapers). These can include novel ideas such as finding out how a good p2p network looks like, and how we can implement corner cases for emergency vehicles (whitelist).


### Student Summary of project deliverables, fallbacks & extensions (student)

#### Deliverables

##### Software

A software package hosted on GitHub containing I/O for input video, licenase plate recognition algorithms (e.g. OpenALPR), networking, and result publishing.

This will most likely be done in C++, PHP, MySQL.

A demo would also be beneficial to show off the project as code is hard to get excited at during a presentation.

##### Hardware

A hardware package will likely be done on a Raspberry Pi Model B, with a camera with a infra-red flash for night time. 


#### Fallbacks

Fallbacks include reverting to software-only implementations. There are already existing license plate recognition software packages (OpenALPR). A centralised server can be easily set up to record license plates and speeds.

As camera input can be faked using pre-recorded input video, running the software onto the Raspberry Pi should be a reasonable expectation. A pure software implementation running on a desktop would be the last resort for demo purposes.

#### Extensions

Multiple extensions are possible with this project, some of which are already defined in the project brief.

Standalone speed detection is a good extension as it tackles the problem of there being only one device in an area with limited deployment. Some target zones can be placed onto the image to track the geometry changes of the license plate, however this may use more processing power. 

Automatic decentralised p2p finding can also be improved, with automatic discovery similar to how a phone finds wifi signals. When found, the device should share its existing database of license plates and calculate the speed using the Google Maps API or similar.

Encryption and privacy concerns can be addressed, first by literature review, then by implementing existing encryption libraries. It is not feasible, nor in the scope of this project, to define a custom encryption scheme.

Lastly, a nice software package should be made on GitHub, maybe a web page or something similar. However this is entirely optional and only serves as flair.


### Summary of Risks (student)

As this project involves software and hardware, there is less time devoted to the algorithmic side of the project than software only projects. Hence, this project will likely use existing libraries to speed up the development process. Rewriting existing libraries is both time consuming and unnecessary.

Hence, a common risk of this is that this might turn into a implementation only project where the entire project is stitching together existing software libraries. To combat this, an emphasis should be placed on novelty. For example, the p2p decentralised protocol and the spatial awareness of the device is a good novel idea. Having a white-list of emergency vehicles depending on the device's location is another one. Reliability improvements using more image processing techniques is also viable.

Another risk of this project is not thoroughly verifying the implementation. As this project involves a camera and real world usage, there should be an emphasis put on testing it in the real world. Low light, bright sunlight, glare, complete darkness should be environments that should be considered. However, time management is critical for this as testing can be time consuming.