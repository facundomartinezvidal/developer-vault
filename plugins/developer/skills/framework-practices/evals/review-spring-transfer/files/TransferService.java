@Service
public class TransferService {
    @Autowired private AccountRepository accounts;
    private final RestTemplate rest = new RestTemplate();

    public void transfer(long from, long to, double amount) {
        doTransfer(from, to, amount);
        rest.postForObject("http://audit/events", from + ":" + to, String.class);
    }

    @Transactional
    private void doTransfer(long from, long to, double amount) {
        Account a = accounts.findById(from).orElseThrow();
        Account b = accounts.findById(to).orElseThrow();
        a.setBalance(a.getBalance() - amount);
        accounts.save(a);
        b.setBalance(b.getBalance() + amount);
        accounts.save(b);
    }
}
