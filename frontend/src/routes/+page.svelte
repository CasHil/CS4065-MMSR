<script lang="ts">
    import Textfield from '@smui/textfield';
    import Button, {Label} from '@smui/button';
	import SearchResult from '../components/SearchResult.svelte';

    let query = '' 
    let performedQuery = '';
    let songResults: string | string[]  = '';
    const matchRelevantSongs = async (query: string) => {
        performedQuery = query;
        songResults = '';
        const response = await fetch('http://localhost:5000/', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    });
        if (!response.ok) {
            songResults = 'Invalid result';
            return;
        }
        const data = await response.json();
        console.log(data.songs)
        songResults = (data.songs as string[]);
        } 
</script>

<style>
    .container {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        height: 100%;
    }

    .left {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 50%;
        height: 100vh;
        margin: 20px;
    }

    .right {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 50%;
        height: 100vh;
        background-color: #f1f1f1;
        margin: 20px;
    }
    
    h1, h2, p, span {
        font-family: 'Roboto', sans-serif;
    }

</style>
<!-- Split the page up in two parts -->
<div class="container">
    <div class="left">
        <h1>Search for music by context</h1>
            <Textfield
              style="width: 100%; margin-bottom: 20px;"
              textarea
              bind:value={query}
              label="Type a context to search music for..."
            >   
            </Textfield>
            <Button on:click={() => matchRelevantSongs(query)} variant="raised">
                <Label>Search</Label>
              </Button>    
    </div>
    <div class="right">
        <h1>Result</h1>
        {#if songResults === 'Invalid song'}
            <p>No songs found for query: {performedQuery}</p>
        {:else if Array.isArray(songResults) && songResults.length > 0}
            {#key songResults}
                <SearchResult songResults={songResults} performedQuery={performedQuery} /> 
            {/key}
        {:else}
            <p>No results yet...</p>
        {/if}
    </div>
</div>