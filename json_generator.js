
      function extractOpportunitiesAndChallenges(htmlString) {
        const parser = new DOMParser();
        const content = parser.parseFromString(htmlString, 'text/html');

        const opportunitiesList = content.querySelector('.opportunities-list + ol');
        const challengesList = content.querySelector('#challenges + ol');

        const opportunities = [];
        const challenges = [];

        if (opportunitiesList) {
          opportunitiesList.querySelectorAll('li').forEach(item => {
            opportunities.push(item.textContent.trim());
          });
        }

        if (challengesList) {
          challengesList.querySelectorAll('li').forEach(item => {
            challenges.push(item.textContent.trim());
          });
        }

        return { opportunities, challenges };
      }


        const climateItems = document.getElementsByClassName('climate-item-unique-id');
        const climateData = [];

        for (const item of climateItems) {
          const expandedContent = item.querySelector('.climate-item-expanded-content')?.innerHTML;
          const { opportunities, challenges } = extractOpportunitiesAndChallenges(expandedContent);

          const climateItem = {
            id: item.id,
            image: item.querySelector('.climate-item-image')?.src,
            category: item.querySelector('.climate-item-category')?.textContent,
            title: item.querySelector('.climate-item-title')?.textContent,
            description: item.querySelector('.climate-item-description')?.textContent,
            overallScore: item.querySelector('.climate-item-overall-score')?.textContent,
            costScore: item.querySelector('.climate-item-cost-score')?.textContent,
            scalabilityScore: item.querySelector('.climate-item-scalability-score')?.textContent,
            publicSupportScore: item.querySelector('.climate-item-public-support-score')?.textContent,
            governmentSupportScore: item.querySelector('.climate-item-government-support-score')?.textContent,
            workforceScore: item.querySelector('.climate-item-workforce-score')?.textContent,
            opportunities,
            challenges
          };
          climateData.push(climateItem);
        }


      const jsonData = JSON.stringify(climateData, null, 2);
      const blob = new Blob([jsonData], {type: 'application/json'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'climate-data.json';
      a.click();
      URL.revokeObjectURL(url);
