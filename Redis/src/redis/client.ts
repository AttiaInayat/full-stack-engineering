import {createClient} from 'redis'


const redisURL = process.env.REDIS_URL

export const  redisClient = createClient({url: redisURL})


redisClient.on("connect",()=>{
    console.log("Redis client connected.")

})

redisClient.on("ready",()=>{
    console.log("Redis client ready.")
    
})

redisClient.on("error",(error)=>{
    console.log("Redis client error: ",error)
    
})

redisClient.on("end",()=>{
    console.log("Redis client connection ended.")
    
})


export async function connectRedis(): Promise<void> {
    if(!redisClient.isOpen){
        await redisClient.connect();
    }

    const ping = await redisClient.ping();
    console.log("ping: ",ping)


}

export async function disconnectRedis(): Promise<void> {
    if(redisClient.isOpen){
        await redisClient.quit();
    }

}
