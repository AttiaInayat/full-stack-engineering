import dotenv from "dotenv"
import {createClient} from 'redis'


dotenv.config()

const redisURL = process.env.REDIS_URL

const redis = createClient({url:redisURL})

async function run(){
    await redis.connect();
    console.log("connected to redis")
    console.log("ping: ", await redis.ping())



//string
const stringKey = "demo:page_views"
await redis.set(stringKey,"100")
const pageviews = await redis.get(stringKey)
console.log(pageviews)

const afterIncr = await redis.incr(stringKey)
console.log(afterIncr)
//hash
const hashKey = "demo:user:profile"

await redis.hSet(hashKey,{
    name: "attia",
    city: "lahore"

})
const extractProfileInfo = await redis.hGetAll(hashKey)
console.log(extractProfileInfo)

//set

const setKey = "demo:tags";

await redis.sAdd(setKey,"nodejs")
await redis.sAdd(setKey,"nextjs")

const tagCount = redis.sCard(setKey)
console.log(tagCount)

//sorted set
const rankKey= "demo:leaderboard"

await redis.zAdd(rankKey,{score: 100, value: "player_a"})
await redis.zAdd(rankKey,{score: 200, value: "player_b"})

const newScore = await redis.zIncrBy(rankKey, 50 , "player_a")
console.log(newScore)

const rank = await redis.zRevRank(rankKey,"player_a")
console.log(rank)

//list
const listKey = "demo:message"
await redis.lPush(listKey,"hello")
await redis.rPush(listKey,"attia")
const extractMessages = await redis.lRange(listKey, 0 , -1)
console.log(extractMessages)

//ttl
const ttlKey = "demo:ttl"
await redis.set(ttlKey,'123456')
await redis.expire(ttlKey,60)
const remainingTime = redis.ttl(ttlKey)
console.log(remainingTime)

await redis.quit()

}

run().catch((error)=>{
    console.log("error: ", error)
    process.exit(1)

})