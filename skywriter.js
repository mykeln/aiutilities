/* this script crawls over an existing page, looks for an element, fires off a prompt to chatgpt based on the contents of said element, then injects the results into the appropriate place */
/* this script is intended to be run once, essentially to generate DOM, not continually hammer the chatgpt api on refresh */
    const OPENAI_API_KEY = 'sk-';

    async function delay(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }


    async function fetchSummary(prompt) {
      console.log('Fetching summary from GPT-3.5-turbo...');
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${OPENAI_API_KEY}`
        },
        body: JSON.stringify({
          model: "gpt-3.5-turbo",
          messages: [
            {
              role: "user",
              content: `Summarize the following climate change technology or practice: "${prompt}"`,
            },
          ],
          max_tokens: 50,
          n: 1,
          stop: null,
          temperature: 0.5,
        })
      });

      const data = await response.json();
      console.log(JSON.stringify(data, null, 2));
      const summary = data.choices[0].message.content.trim();
      console.log('Summary fetched:', summary);
      return summary;
    }

    async function summarizeAndInsertParagraph(thElement) {
      console.log('Reading contents of the <th> element...');
      const thContent = thElement.textContent;

      console.log('Fetching summary...');
      const summary = await fetchSummary(thContent);

      console.log('Creating new paragraph element...');
      const newParagraph = document.createElement('p');
      newParagraph.textContent = summary;

      console.log('Finding associated <tr class="climate-item-expanded-content"> after the <th> element...');
      const associatedTr = thElement.closest('tr').nextElementSibling;
      if (associatedTr && associatedTr.classList.contains('expanded-content')) {
        console.log('Inserting new paragraph immediately after the opening of the "expanded-content" div');
        const firstChild = associatedTr.querySelector('td > :first-child');
        if (firstChild) {
          firstChild.insertAdjacentElement('beforebegin', newParagraph);
        } else {
          const tdElement = associatedTr.querySelector('td');
          if (tdElement) {
            tdElement.appendChild(newParagraph);
          }
        }
      } else {
        console.log('No <tr class="climate-item-expanded-content"> found. Inserting new paragraph after the <th> element');
        thElement.insertAdjacentElement('afterend', newParagraph);
      }
    }


    (async () => {
      console.log('Starting...');

      const climateItems = document.querySelectorAll('th.climate-item');
      for (const climateItem of climateItems) {
        await summarizeAndInsertParagraph(climateItem);
        await delay(1000);
      }

      console.log('Done!');
    })();