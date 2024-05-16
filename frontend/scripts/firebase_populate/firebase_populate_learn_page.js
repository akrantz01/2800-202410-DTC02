import {
  addDoc,
  collection,
} from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js';

import { firestore } from '../firebase.js';

const biases = [
  {
    name: 'Confirmation Bias',
    description:
      "The tendency to search for, interpret, favor, and recall information in a way that confirms one's preexisting beliefs or theories.",
    example:
      'A person who believes in astrology might only remember the instances when horoscopes seemed accurate and ignore the times they were wrong.',
    impact:
      'It can lead to a skewed perception of reality, reinforcing incorrect beliefs and making it difficult to consider alternative viewpoints.',
  },
  {
    name: 'Anchoring Bias',
    description:
      "The tendency to rely too heavily on the first piece of information encountered (the 'anchor') when making decisions.",
    example:
      'If a person sees a T-shirt priced at $1,000 and then sees another one for $100, they may perceive the second T-shirt as cheap.',
    impact:
      'It can affect negotiations, pricing strategies, and decision-making processes by unduly influencing judgments.',
  },
  {
    name: 'Halo Effect',
    description:
      'The tendency for an impression created in one area to influence opinion in another area.',
    example: 'If someone is attractive, people may also assume they are intelligent and kind.',
    impact:
      'It can lead to biased assessments of individuals, particularly in hiring, promotions, and performance evaluations.',
  },
  {
    name: 'Framing Effect',
    description:
      'The tendency to react to a particular choice based on how it is presented, e.g., as a loss or as a gain.',
    example:
      'People are more likely to choose a surgery with a 90% survival rate than one with a 10% mortality rate, even though they are the same.',
    impact:
      'It can influence decisions in marketing, policy-making, and everyday choices by altering perceptions.',
  },
  {
    name: 'Negativity Bias',
    description:
      'The tendency to give more weight to negative information than positive information.',
    example: 'People tend to remember criticisms more than compliments.',
    impact:
      'It can lead to an overly pessimistic view of situations, affecting mental health and decision-making.',
  },
  {
    name: 'Availability Heuristic',
    description:
      'The tendency to overestimate the likelihood of events based on their availability in memory, which is often influenced by recent or vivid events.',
    example:
      'After seeing news reports about airplane crashes, people might think air travel is more dangerous than it is.',
    impact: 'It can distort risk assessments and lead to irrational fears or overreactions.',
  },
  {
    name: 'Selection Bias',
    description:
      'The bias introduced by the selection of individuals, groups, or data for analysis in such a way that proper randomization is not achieved.',
    example:
      'Surveying only those who visit a particular website might not represent the general population.',
    impact:
      'It can lead to inaccurate conclusions and undermine the validity of research findings.',
  },
  {
    name: 'Survivorship Bias',
    description:
      "The logical error of concentrating on the people or things that 'survived' some process and overlooking those that did not because of their lack of visibility.",
    example:
      'Studying successful companies without considering failed ones can lead to incorrect conclusions about business success.',
    impact:
      'It can create a false sense of understanding and success, leading to misguided decisions.',
  },
  {
    name: 'Bandwagon Effect',
    description: 'The tendency to adopt beliefs and ideas because many others do.',
    example:
      'People might start believing in a fad diet because it is popular, not because it is scientifically sound.',
    impact: 'It can lead to conformity and suppress individual critical thinking.',
  },
  {
    name: 'Overconfidence Bias',
    description:
      "The tendency to be more confident in one's own abilities, such as driving, teaching, or spelling, than is objectively warranted.",
    example:
      'A person might believe they can complete a project in a week when it realistically takes a month.',
    impact: 'It can result in underestimating risks, overcommitting, and poor decision-making.',
  },
];

async function populateBiases() {
  const biasesCollection = collection(firestore, 'biases');
  for (const bias of biases) {
    await addDoc(biasesCollection, bias);
  }
  console.log('Biases have been added to Firebase');
}

populateBiases();
