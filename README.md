# CopyeditGPT
A Flask app that sends text to OpenAI for copy editing. 

<h2>Welcome to CopyeditGPT!</h2>
This project helps you utilize OpenAI's GPT3 engine to copy edit your documents. Submit a .txt file with writing of any kind, and the site will return a document that has been edited for spelling, grammar, punctuation, syntax, and other specifications of the Chicago Manual of Style. 

While ChatGPT and the OpenAI API have length limitations for submissions, this web app will handle almost any length behind the scenes, breaking down large documents into chunks of about one thousand words, submitting them in successive API calls, then returning the results in one file. Be mindful that this app breaks documents down by paragraph, so if your document has huge paragraphs (specifically, two successive paragraphs totaling more than about 1500 words), then it may resort in an error. 

<h3>How to Use</h3>
You will need:
1. An OpenAI API key.<br>
2. Your writing in a .txt file.<br>
3. Patience (especially with long documents)<br>

<h4>API Key</h4>

If you don't have an API key, head to <a href="https://platform.openai.com/account/api-keys/" target="_blank">OpenAI's API page</a> and create an account. You will also need to set up a payment method, as the API does cost a negligible amount for usage.

How much does it cost? The short answer is, very little.<br>
This app is using the Davinci-003 model, which costs $0.03 per one thousand tokens of usage. Analysis of one thousand words will use about 2,500 tokens. So, editing a full-length article will run you about ten cents. A novel of one hundred thousand words will run you about half the cost of a cup of coffee.

<h4>.txt Files</h4>
Currently this editor only accept .txt files, as I am still working to ensure it provides consistently formatted results. It should soon be accepting .docx, .doc, and other text files, as I will be exploring which Python modules are most useful here.

<h4>Patience</h4>
A submission of a thousand words takes about fifteen to thirty seconds to process, depending on the time of day. If you have to stare at a loading wheel for a while, just imagine what it was like being a programmer in 1990 trying to download an entire megabyte of data.

<h3>How to Process Your Results</h3>
You will get back a .txt with corrections made at GPT-3's discretion. You will want to compare this to your old document and choose which changes to keep or reject. For that, you can use Microsoft Word's compare tool, under the review panel.

<h3>How to Contribute to this Project</h3>
Please contribute!

This project still has a lot of room for improvement, and I hope to see it through. So if you're looking for an open source Flask project that will be easy to jump into, this is a great choice! 

<h4>Aspects that need to be implemented or improved:</h4>
<h4>More modern frontend framework and design.</h4> 
I'm open to any ideas here. This site has a little bit of Bootstrap usage. Otherwise this is just plain HTML and needs a lot of work. We need more robust error message feedback for incorrect entries, including incorrect files, exceeding limitations, incorrect API keys, etc.
<h4>Progress bar</h4>
An interim page to provide feedback on the progress as the document is processing. At the very least, a process which counts the words of the submission then updates the user on what percent has been processed with each API call (which processes about a thousand words at a time).
<h4>.docx and .doc compatibility</h4>
I would like to use the Aspose.Words library to receive text in .docx files. I am not sure if there is a way to return a document to the user that shows the GPT-3 changes as a markup, but if that is possible this must be implemented!
<h4>Ability to customize prompts and depth of editing</h4>
Currently, the settings on the API call are fixed, but it would not be difficult to implement a frontend panel which lets the client alter some of the settings. They may want to alter the prompt, changes which style guide to follow, dial up the "temperature," or alter other settings. These will need to be succinctly explained to the user and made easy to alter through a menu.
<h4>User registration and file storage</h4>
The user should be able register a username and navigate to the results page and download their edited files at anytime from a database. SQLAlchemy needs to be built in for storing binary files generated in the results section. 
<h4>Handle paragraphs of any length</h4>
Currently my method for breaking apart large text files is to split them by paragraph (or by "\n" characters). This ensures a simple method for breaking apart the text while still retaining some of the formatting, in case the user just wants to read their results on the page, or if they don't have a way to compare docs. However, in rare cases where a paragraph is over a thousand words, the editing process will be prevented by the API's token limit. A more sophisticated approach could split the text first by "\n" then break it down into another layer of split apart words, but seeing as this will help to accommodate rare types of writing, it has not yet been implemented.
<h3>Thanks for reading!</h3>
Please give the app a try and review my code! This is my first ever coding project. I have a lot to learn and would very much like to work with others who can provide constructive criticism to help improve my abilities.<br>

