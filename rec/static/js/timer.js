function timer(){

    let times = document.getElementsByClassName("timer");
    for(let i=0; i<times.length; i++){
        let hours = Number.parseInt(times[i].innerHTML.substr(0,2), 10);
        let minutes = Number.parseInt(times[i].innerHTML.substr(3,2), 10);
        let seconds = Number.parseInt(times[i].innerHTML.substr(6,2), 10);
        if(seconds+1>59)
        {
            seconds = 0;
            if(minutes+1>59)
            {
                minutes = 0;
                hours++;
            }
            else
                minutes++;
        }
        else
            seconds++;

        if(hours<10)
            hours = '0'+hours;
        if(minutes<10)
            minutes = '0'+minutes;
        if(seconds<10)
            seconds = '0'+seconds;

        times[i].innerHTML = hours+":"+minutes+":"+seconds;
    }

    setTimeout(timer, 1000)
}
timer();

