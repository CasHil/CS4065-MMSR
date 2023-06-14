<script lang="ts">
    import Textfield from '@smui/textfield';
    import Button, {Label} from '@smui/button';
	import SearchResult from '../components/SearchResult.svelte';
    import {writable} from 'svelte/store';
    
    let query = '' 
    let songResult  = '';
    const search = async (query: string) => {
        
        const response = await fetch('http://localhost:5000/', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    });
        const data = await response.json();
        songResult = data.song;
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
    
    h1 {
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
            <Button on:click={() => search(query)} variant="raised">
                <Label>Search</Label>
              </Button>    </div>
    <div class="right">
        <h1>Result</h1>
        {#if songResult}
            <SearchResult result={songResult} /> 
        {:else}
            <p>No results yet...</p>
        {/if}
    </div>
</div>