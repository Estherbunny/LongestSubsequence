<h2>API and Frontend for Longest Increasing Subsequence</h2>
<p>The code in this directory creates the website found at
<a href="http://54.84.243.150/">http://54.84.243.150/</a></p>

<p>It consists of two parts, a REST API call, and a web interface.</p>

<h3>REST API call</h3>

<p>The REST API call takes as input a sequence of integers, and outputs the longest increasing subsequence within that sequence of integers. There is an optional <code>verbose</code> parameter which allows you to receive a list of indexes of the longest increasing subsequence numbers within the original sequence, along with runtime information.</p>

<p>An example API call is:</p>

<code>curl -H "Content-Type: application/json" -X POST -d '{"num_array":"1,4,5,6,2,1,5,7,3","verbose":1}' http://54.84.243.150/api/longest/</code>

<p>and the resulting JSON output is</p>

<code>{"indexes": "0,1,2,3,7", "time": "3.2901763916e-05", "out": "1,4,5,6,7"}</code>

<p>If called without the <code>verbose</code> parameter (or with <code>"verbose":0</code> or <code>"verbose":false</code>), then the call and output is simply:

<code>curl -H "Content-Type: application/json" -X POST -d '{"num_array":"1,4,5,6,2,1,5,7,3"}' http://54.84.243.150/api/longest/</code>

<p>and the resulting JSON output is</p>

<code>{"out": "1,4,5,6,7"}</code>

<p>The algorithm which powers the API is found in the file</p>

<a href="https://github.com/Estherbunny/LongestSubsequence/blob/master/sequence/sequence/views.py">/sequence/sequence/views.py</a>

<p>It is an <i>O (n log n)</i> implementation</p> of finding the longest increasing subsequence</p>



<h3>Web Frontend</h3>



<h2>Directory Structure</h2>





