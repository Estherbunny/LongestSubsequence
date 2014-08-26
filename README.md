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

<p>If called without the <code>verbose</code> parameter (or with <code>"verbose":0</code> or <code>"verbose":false</code>), then the call and output is simply:</p>

<code>curl -H "Content-Type: application/json" -X POST -d '{"num_array":"1,4,5,6,2,1,5,7,3"}' http://54.84.243.150/api/longest/</code>

<p>and the resulting JSON output is</p>

<code>{"out": "1,4,5,6,7"}</code>

The error codes

<h4>Algorithm</h4>

<p>The algorithm which powers the API is found in the file</p>

<a href="https://github.com/Estherbunny/LongestSubsequence/blob/master/sequence/sequence/views.py">/sequence/sequence/views.py</a>

<p>It is an <i>O (n log n)</i> implementation of finding the longest increasing subsequence. It is easy to see that there exists an <i>O (n^2)</i> solution to the problem of finding the longest increasing subsequence in an input sequence <i>x<sub>0</sub>,x<sub>1</sub>,...x<sub>n-1</sub></i>. First, let's present that.</p>

<p>Let <i>L(i)</i> represent the longest increasing subsequence at index <i>i</i> of our input sequence. Then <i>L(i)=0</i> if <i>i=0</i>, and <i>L(i) = 1 + max<sub>j=0,...,(i-1)</sub>L(j)</i> if <i>x<sub>j</sub> &lt; x<sub>i</sub></i> and <i>i>0</i>. One can then use dynamic programming to create an array of size <i>n</i> which stores <i>L(i)</i>, and then for each <i>i</i>, traversed in order, the values of all <i>L(j)</i> and <i>x<sub>j</sub></i> (where <i>j &lt; i</i>) can be used to determine the value of <i>L(i)</i>.  This traversal of up to <i>n</i> previous data points, for each of the <i>n</i> data points gives rise to an <i>O (n^2)</i> runtime.</p>

<p>As we traverse the <i>j = 0,1,...,(i-1)</i> elements in for every <i>i</i>, it should become apparent that we are only interested in some "best case" previous scenarios, and all <i>j</i> that are not these "best case" scenarios are irrelevant. This "best case" for each potential longest-sequence found in <i>x<sub>0</sub>,x<sub>1</sub>,...x<sub>i-1</sub></i> consist of the smallest values <i>x<sub>j</sub></i> (where <i>j &lt; i</i>) which form the final integer in a longest subsequence of length <i>m</i>, for all <i>0 &le; m &le; M</i>, where <i>M</i> is the length of the largest subsequence found thus far. </p>

<h3>Web Frontend</h3>

<p>The web frontend is powered by a <a href="https://github.com/Estherbunny/LongestSubsequence/blob/master/templates/frontend/home.html">template file</a>, <a href="https://github.com/Estherbunny/LongestSubsequence/blob/master/sequence/frontend/views.py">views.py file</a>, and <a href="https://github.com/Estherbunny/LongestSubsequence/blob/master/sequence/frontend/models.py">models.py</a> file.</p>

<p>Additionally, the open source Javascript library <a href="http://www.jqplot.com/index.php">jqPlot</a> was used to make  graphs of the input numbers and the resulting longest increasing subsequence.</p>



<h2>Directory Structure</h2>





