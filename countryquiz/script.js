// variables
let startButton = document.getElementById('startbutton');
let firstScreen = document.getElementById('firstscreen');
let questionScreen = document.getElementById('questionscreen')
let quizquestion = document.getElementById('quizquestion')
let countryImage = document.getElementById('countryimage')
let questionContainer = document.getElementById('questioncontainer')
let choices = document.getElementsByClassName('choice')
let nextButton = document.getElementById('optionswhenanswered')
let wrongCapitals = []
let wrongNames = []
let result = document.getElementById('result')
let resultMarks = document.getElementById('resultmarks')

//get the data 
let request = new XMLHttpRequest ; 
request.open('GET' , 'countriesV3.json')
request.send()
request.onload = ()=>{
	let javaObject = JSON.parse(request.response)
	let country = javaObject[Math.floor(Math.random()*250)]

	// get a list of capitals and country names
	for(let c in javaObject){
		if (javaObject[c].capital.length>1){
			wrongCapitals.push(javaObject[c].capital.join(' , '))
		}else if (javaObject[c].capital.length==0){
			wrongCapitals.push('this country has no capital')
		}else if (javaObject[c].capital.length==1){
			wrongCapitals.push(javaObject[c].capital[0])
		}
		wrongNames.push(javaObject[c].name.common)
	}
	// onclick
	startButton.addEventListener('click',()=>{
		firstScreen.style.display='none';
		questionScreen.style.display='flex'
		questionContainer.style.justifyContent='flex-start'
		
		let ques_no=1
		let correctCount = 0
		//random question generator
		for (i=0 ; i<ques_no ; i++){	
			let check = false ;
			let rightChoice = Math.floor(Math.random()*4)
			country = javaObject[Math.floor(Math.random()*251)]
			let question = randomQuestions[Math.floor(Math.random()*3)]
			if (question == 'what is the capital of'){
				quizquestion.innerText=`${i+1} - what is the capital of ${country.name.common}`
				countryImage.src=''
				if (country.capital.length == 0){
					choices[rightChoice].innerText =  'this country has no capital'
					for(let j in choices){
						if(j == rightChoice){
							continue
						}else{
							if(choices[j].innerText!==undefined){
								let randomInt = Math.floor(Math.random()*250)
								if(wrongCapitals[randomInt] !== choices[rightChoice].innerText){
									choices[j].innerText=wrongCapitals[randomInt]
								}else{
									randomInt = Math.floor(Math.random()*250)
									choices[j].innerText=wrongCapitals[randomInt]
								}
							}
						}
					}
				}else if (country.capital.length == 1){
					choices[rightChoice].innerText = `${country.capital[0]}`
					for(let j in choices){
						if(j == rightChoice){
							continue
						}else{
							if(choices[j].innerText!==undefined){
								let randomInt = Math.floor(Math.random()*250)
								if(wrongCapitals[randomInt] !== choices[rightChoice].innerText){
									choices[j].innerText=wrongCapitals[randomInt]
								}else{
									randomInt = Math.floor(Math.random()*250)
									choices[j].innerText=wrongCapitals[randomInt]
								}
							}
						}
					}
				}else {
					choices[rightChoice].innerText = `${country.capital.join(' , ')}`
					for(let j in choices){
						if(j == rightChoice){
							continue
						}else{
							if(choices[j].innerText!==undefined){
								let randomInt = Math.floor(Math.random()*250)
								if(wrongCapitals[randomInt] !== choices[rightChoice].innerText){
									choices[j].innerText=wrongCapitals[randomInt]
								}else{
									randomInt = Math.floor(Math.random()*250)
									choices[j].innerText=wrongCapitals[randomInt]
								}
							}
						}
					}
				}
			}else if (question == 'what is the name of this country'){
				quizquestion.innerText = `${i+1} - what is the name of this country`
				countryImage.src=country.flags[1]
				choices[rightChoice].innerText = `${country.name.common}`
				for(let j in choices){
					if(j == rightChoice){
						continue
					}else{
						if(choices[j].innerText!==undefined){
							let randomInt = Math.floor(Math.random()*250)
							if(wrongNames[randomInt] !== choices[rightChoice].innerText){
								choices[j].innerText=wrongNames[randomInt]
							}else{
								randomInt = Math.floor(Math.random()*250)
								choices[j].innerText=wrongNames[randomInt]
							}
						}
					}
				}
			}else if (question == "what is the country that it's capital is"){
				countryImage.src=''
				if (country.capital.length == 0){
					quizquestion.innerText = `${i+1} - what is the country that has no capital`
					choices[rightChoice].innerText = `${country.name.common}`
				}else if (country.capital.length == 1){
					quizquestion.innerText = `${i+1} - what is the country that it's capital is ${country.capital[0]}`
					choices[rightChoice].innerText = `${country.name.common}`
				}else {
					quizquestion.innerText = `${i+1} - what is the country that it's capitals are ${country.capital.join(' , ')}`
					choices[rightChoice].innerText = `${country.name.common}`
				}
				for(let j in choices){
					if(j == rightChoice){
						continue
					}else{
						if(choices[j].innerText!==undefined){
							let randomInt = Math.floor(Math.random()*250)
							if(wrongNames[randomInt] !== choices[rightChoice].innerText){
								choices[j].innerText=wrongNames[randomInt]
							}else{
								randomInt = Math.floor(Math.random()*250)
								choices[j].innerText=wrongNames[randomInt]
							}
						}
					}
				}
			}
			let state = true
			for(let cc in choices){
				choices[cc].onclick = ()=>{
					nextButton.style.display='block'
					if (state){
						if (choices[cc].innerText!==undefined && choices[cc].style.backgroundColor == ''){
							if(cc == rightChoice){
								choices[cc].style.backgroundColor='#00EA90'
								correctCount++
							}else{
								for (let ccc in choices){
									if(choices[ccc].innerText!==undefined){
										if (ccc == rightChoice){
											choices[ccc].style.backgroundColor='#00EA90'
										}else{
											if(choices[ccc].innerText !== undefined){
												choices[ccc].style.backgroundColor='#ED403B'
											}
										}
									}
								}
							}
						}
						state=false
					}
				}
			}
		}
		nextButton.onclick=()=>{
			nextButton.style.display='none'
			if(ques_no <= 9){
				for (let ccc in choices){
					if(choices[ccc].innerText!==undefined){
						choices[ccc].style.backgroundColor='#ddd'
					}
				}
				ques_no++
				for (i=0 ; i<ques_no ; i++){	
					let check = false ;
					let rightChoice = Math.floor(Math.random()*4)
					country = javaObject[Math.floor(Math.random()*251)]
					let question = randomQuestions[Math.floor(Math.random()*3)]
					if (question == 'what is the capital of'){
						quizquestion.innerText=`${i+1} - what is the capital of ${country.name.common}`
						countryImage.src=''
						if (country.capital.length == 0){
							choices[rightChoice].innerText =  'this country has no capital'
							for(let j in choices){
								if(j == rightChoice){
									continue
								}else{
									if(choices[j].innerText!==undefined){
										let randomInt = Math.floor(Math.random()*250)
										if(wrongCapitals[randomInt] !== choices[rightChoice].innerText){
											choices[j].innerText=wrongCapitals[randomInt]
										}else{
											randomInt = Math.floor(Math.random()*250)
											choices[j].innerText=wrongCapitals[randomInt]
										}
									}
								}
							}
						}else if (country.capital.length == 1){
							choices[rightChoice].innerText = `${country.capital[0]}`
							for(let j in choices){
								if(j == rightChoice){
									continue
								}else{
									if(choices[j].innerText!==undefined){
										let randomInt = Math.floor(Math.random()*250)
										if(wrongCapitals[randomInt] !== choices[rightChoice].innerText){
											choices[j].innerText=wrongCapitals[randomInt]
										}else{
											randomInt = Math.floor(Math.random()*250)
											choices[j].innerText=wrongCapitals[randomInt]
										}
									}
								}
							}
						}else {
							choices[rightChoice].innerText = `${country.capital.join(' , ')}`
							for(let j in choices){
								if(j == rightChoice){
									continue
								}else{
									if(choices[j].innerText!==undefined){
										let randomInt = Math.floor(Math.random()*250)
										if(wrongCapitals[randomInt] !== choices[rightChoice].innerText){
											choices[j].innerText=wrongCapitals[randomInt]
										}else{
											randomInt = Math.floor(Math.random()*250)
											choices[j].innerText=wrongCapitals[randomInt]
										}
									}
								}
							}
						}
					}else if (question == 'what is the name of this country'){
						quizquestion.innerText = `${i+1} - what is the name of this country`
						countryImage.src=country.flags[1]
						choices[rightChoice].innerText = `${country.name.common}`
						for(let j in choices){
							if(j == rightChoice){
								continue
							}else{
								if(choices[j].innerText!==undefined){
									let randomInt = Math.floor(Math.random()*250)
									if(wrongNames[randomInt] !== choices[rightChoice].innerText){
										choices[j].innerText=wrongNames[randomInt]
									}else{
										randomInt = Math.floor(Math.random()*250)
										choices[j].innerText=wrongNames[randomInt]
									}
								}
							}
						}
					}else if (question == "what is the country that it's capital is"){
						countryImage.src=''
						if (country.capital.length == 0){
							quizquestion.innerText = `${i+1} - what is the country that has no capital`
							choices[rightChoice].innerText = `${country.name.common}`
						}else if (country.capital.length == 1){
							quizquestion.innerText = `${i+1} - what is the country that it's capital is ${country.capital[0]}`
							choices[rightChoice].innerText = `${country.name.common}`
						}else {
							quizquestion.innerText = `${i+1} - what is the country that it's capitals are ${country.capital.join(' , ')}`
							choices[rightChoice].innerText = `${country.name.common}`
						}
						for(let j in choices){
							if(j == rightChoice){
								continue
							}else{
								if(choices[j].innerText!==undefined){
									let randomInt = Math.floor(Math.random()*250)
									if(wrongNames[randomInt] !== choices[rightChoice].innerText){
										choices[j].innerText=wrongNames[randomInt]
									}else{
										randomInt = Math.floor(Math.random()*250)
										choices[j].innerText=wrongNames[randomInt]
									}
								}
							}
						}
					}
					let stateTwo = true
					for(let cc in choices){
						choices[cc].onclick = ()=>{
							nextButton.style.display='block'
							if(stateTwo){
								if (choices[cc].innerText!==undefined && choices[cc].style.backgroundColor == 'rgb(221, 221, 221)' ){
									if(cc == rightChoice){
										choices[cc].style.backgroundColor='#00EA90'
										correctCount++
									}else{
										for (let ccc in choices){
											if(choices[ccc].innerText!==undefined){
												if (ccc == rightChoice){
													choices[ccc].style.backgroundColor='#00EA90'
												}else{
													if(choices[ccc].innerText !== undefined){
														choices[ccc].style.backgroundColor='#ED403B'
													}
												}
											}
										}
									}
								}
								stateTwo=false
							}
						}
					}
				}
			}else{
				questionScreen.style.display='none'
				result.style.display='flex'
				resultMarks.innerText=`you've got ${correctCount} out of 10`
			}
		}
	}
	
	)
	}	

// question generator 
let randomQuestions = [
	'what is the capital of',
	'what is the name of this country',
	"what is the country that it's capital is"
]


