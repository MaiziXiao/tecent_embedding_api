<pre><code> 
docker build -t linchenxiao/embeddingapi:v1.0.0 .

</code></pre>

<pre><code> docker run \
-v $GOOGLE_APPLICATION_CREDENTIALS:/Users/linchenxiao/gcp_keys/playground-linchen-2774599fb4bc.json:ro \
-e GOOGLE_APPLICATION_CREDENTIALS=/Users/linchenxiao/gcp_keys/playground-linchen-2774599fb4bc.json \
-p 80:80 linchenxiao/embeddingapi:v1.0.0

</code></pre>